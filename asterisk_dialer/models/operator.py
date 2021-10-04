# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
import json
from datetime import datetime, timedelta
from odoo import models, fields, api, _


logger = logging.getLogger(__name__)

OPERATOR_STATES = [
    ('offline', 'Offline'),
    ('available', 'Available'),
    ('connected', 'Connected'),
    ('busy', 'Busy'),
]


class Operator(models.Model):
    _name = 'asterisk_dialer.operator'
    _order = 'user'

    user = fields.Many2one(
        'res.users', required=True,
        help=_("The Odoo user this operator is assotiated with.")
    )
    name = fields.Char(related='user.name')
    accountcode = fields.Char(
        required=True,
        help=_("Accountcode is used to correspond call events to operators."
            "\nSIP endpoint used by this operator must have the same accountcode= setting on Asterisk side."
        )
    )
    channel = fields.Char(default='', readonly=True)
    state = fields.Selection(
        OPERATOR_STATES, default='offline', required=True, readonly=True,
        help=_("Operator's current state. Can be one of: Offline, Available, Connected, Busy.")
    )
    campaign = fields.Many2one(
        'asterisk_dialer.campaign', readonly=True,
        help=_("Current operator's campaign."),
    )
    contact = fields.Many2one(
        'asterisk_dialer.contact', readonly=True,
        help=_("Contact's name, if operator is connected to him.")
    )
    last_session = fields.Char()

    _sql_constraints = [
        ('user_uniq', 'UNIQUE(user)', 'This user is already defined!'),
        ('accountcode_uniq', 'UNIQUE(accountcode)', 'This accountcode is already defined!'),
    ]

    @api.model
    def confbridge_leave(self, event):
        # logger.info('ConfBridgeLeave: %s', json.dumps(event, indent=2))
        channel = self.env['asterisk_dialer.channel'].search(
            [('uniqueid', '=', event['Uniqueid'])])
        operator = self.env['asterisk_dialer.operator'].search(
            [('accountcode', '=', event['BridgeName'])])
        # Update operator status
        if channel.contact:
            operator.write({
                'state': 'available',
                'contact': False,
            })
            channel.contact.write({
                'state': 'd',
            })
            self.env.cr.commit()
            # Hangup the channel as it will remain in AGI otherwise.
            self.env.user.asterisk_agent.action({
                'Action': 'AGI',
                'Channel': channel.channel,
                'Command': 'EXEC HANGUP',
            }, no_wait=True, notify=True)
        elif channel.operator:
            operator_contact = operator.contact
            # Operator channel destroy
            operator.write({
                'state': 'offline',
                'contact': False,
                'campaign': False,
                'channel': '',
            })
            self.env.cr.commit()
            # Hangup the connected channels also
            operator_channel = self.env['asterisk_dialer.channel'].search(
                [('contact', '=', operator_contact.id)])
            for ch in operator_channel:
                self.env.user.asterisk_agent.action({
                    'Action': 'Hangup',
                    'Channel': ch.channel,
                }, no_wait=True, notify=True)
        return True

    @api.model
    def confbridge_join(self, event):
        # logger.info('ConfbridgeJoin: %s', json.dumps(event, indent=2))
        channel = self.env['asterisk_dialer.channel'].search(
            [('uniqueid', '=', event['Uniqueid'])])
        if not channel:
            logger.warning('CHANNEL NOT FOUND FOR CONFBGIDGE JOIN!')
            return False
        # Now update contact connection status.
        if channel.contact:
            # Update connected operator
            operator = self.env['asterisk_dialer.operator'].search(
                [('accountcode', '=', event['BridgeName'])])
            channel.write({'connected_operator': operator.id})
            # Update contact
            channel.contact.write({
                'state': 'c',
            })
            operator.write({
                'state': 'connected',
                'contact': channel.contact})
            channel.campaign.log('Contact {} connected to operator {}'.format(
                channel.contact.name, operator.name))
        # It's operator joining his confbridge. Update his state.
        elif channel.operator:
            channel.operator.write({
                'state': 'available',
            })
            channel.campaign.wakeup()
        return True

    def disconnect(self):
        found = self.env['asterisk_dialer.channel'].search([
            ('operator', '=', self.id)])
        if not found:
            logger.warning('Channel {} not found for hangup.'.format(self.channel))
        # Send AMI Hangup to Asterisk
        logger.info('SENDING HANGUP TO ASTERISK CHANNEL %s',
                    found.channel)
        self.env.user.asterisk_agent.action(
            {'Action': 'Hangup', 'Channel': found.channel},
            notify=True, no_wait=True)
        found.unlink()
        self.write({
            'state': 'offline',
            'channel': '',
            'campaign': False,
            'contact': False,
        })
        return True

    def notify_operator(self, message):
        self.ensure_one()
        self.env['bus.bus'].sendone(
            'dialer_operator_{}'.format(self.accountcode), message)
