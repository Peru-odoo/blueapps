# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
from datetime import datetime, timedelta
import json
import logging
import uuid
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
try:
    import humanize
    HUMANIZE = True
except ImportError:
    HUMANIZE = False

logger = logging.getLogger(__name__)


class Channel(models.Model):
    _name = 'asterisk_dialer.channel'
    _rec_name = 'channel'
    _description = 'Active Channel'
    _order = 'id desc'

    # Asterisk fields
    channel = fields.Char(index=True)
    uniqueid = fields.Char(size=150, index=True)
    linkedid = fields.Char(size=150, index=True)
    context = fields.Char(size=80)
    connected_line_num = fields.Char(size=80)
    connected_line_name = fields.Char(size=80)
    state = fields.Char(size=80)
    state_desc = fields.Char(size=256, string=_('State'))
    exten = fields.Char(size=32)
    callerid_num = fields.Char(size=32)
    callerid_name = fields.Char(size=32)
    system_name = fields.Char(size=32)
    accountcode = fields.Char(size=80)
    priority = fields.Char(size=4)
    timestamp = fields.Char(size=20)
    app = fields.Char(size=32, string='Application')
    app_data = fields.Char(size=512, string='Application Data')
    language = fields.Char(size=2)
    event = fields.Char(size=64)
    # Hangup event fields
    cause = fields.Char(index=True)
    cause_txt = fields.Char(index=True)
    # Not Asterisk fields
    active = fields.Boolean(default=True, index=True)
    operator = fields.Many2one('asterisk_dialer.operator', ondelete='set null')
    contact = fields.Many2one('asterisk_dialer.contact', ondelete='set null')
    campaign = fields.Many2one('asterisk_dialer.campaign', ondelete='cascade')
    start_time = fields.Datetime(default=fields.Datetime.now, index=True)
    end_time = fields.Datetime(index=True)
    duration = fields.Integer(compute='_get_call_duration', store=True)
    duration_human = fields.Char('Duration', compute='_get_humanized_duration')
    start_time_human = fields.Char('Start Time', compute='_get_humanized_start_time')
    connected_operator = fields.Many2one('asterisk_dialer.operator', ondelete='set null')

    @api.depends('start_time', 'end_time')
    def _get_call_duration(self):
        for rec in self:
            if not rec.end_time:
                rec.duration = False
            else:
                rec.duration = int(
                    (rec.end_time - rec.start_time).total_seconds())

    def _get_humanized_duration(self):
        global HUMANIZE
        if HUMANIZE:
            try:
                to_translate = self.env.context.get('lang', 'en_US')
                if to_translate != 'en_US':
                    humanize.i18n.activate(to_translate)
            except Exception:
                HUMANIZE = False
        for rec in self:
            if HUMANIZE:
                if rec.duration:
                    rec.duration_human = humanize.naturaldelta(rec.duration)
                else:
                    rec.duration_human = ''
            else:
                rec.duration_human = str(rec.duration)

    def _get_humanized_start_time(self):
        global HUMANIZE
        if HUMANIZE:
            try:
                to_translate = self.env.context.get('lang', 'en_US')
                if to_translate != 'en_US':
                    humanize.i18n.activate(to_translate)
            except Exception:
                HUMANIZE = False
        for rec in self:
            if HUMANIZE:
                if rec.duration > 0:
                    rec.start_time_human = humanize.naturaltime(fields.Datetime.from_string(rec.start_time))
                else:
                    rec.start_time_human = ''
            else:
                rec.start_time_human = '{}'.format(rec.duration or '')


    def unlink(self):
        res = False
        if self.env.context.get('ami_hangup'):
            # Send AMI Hangup to Asterisk
            for channel in self:
                logger.info('SENDING HANGUP TO ASTERISK CHANNEL %s',
                            channel.channel)
                self.env.user.asterisk_agent.action(
                    {'Action': 'Hangup', 'Channel': channel.channel},
                    notify=True, no_wait=True)
            if self.env.context.get('no_unlink'):
                # Don't remove channels as they will be removed by Asterisk.
                return True
        # Update operator and contact statuses
        campaigns_to_wakeup = {}
        for rec in self:
            if rec.operator:
                # Reset operator channel
                rec.operator.write({
                    'state': 'offline',
                    'channel': '',
                    'campaign': False
                })
            if rec.campaign:
                campaigns_to_wakeup[rec.campaign] = rec.campaign
        # Archive channel first, delete archived channels
        for rec in self:
            if not rec.active:
                res = super(Channel, rec).unlink()
            else:
                rec.active = False
                res = True
        # Do the work!
        self.env.cr.commit()
        try:
            for c in campaigns_to_wakeup:
                c.wakeup()
        finally:
            return res

    @api.model
    def originate(self, channel=None, app=None, data=None, sync=False,
                  operator=False, campaign=False, contact=False):
        channel_id = uuid.uuid4().hex
        other_channel_id = uuid.uuid4().hex
        self.create({
            'uniqueid': channel_id,
            'linkedid': other_channel_id,
            'operator': operator,
            'campaign': campaign.id,
            'contact': contact.id,
        })
        # Commit as new channel will come very quickly :-)
        self.env.cr.commit()
        logger.info('ORIGINATE FOR CAMPAIGN %s TO CONTACT ID %s.',
                    campaign.name, contact.id)
        self.env.user.asterisk_agent.action({
            'Action': 'Originate',
            'Channel': channel,
            'Application': app,
            'Async': str(not sync).lower(),
            'ChannelId': channel_id,
            'OtherChannelId': other_channel_id,
            'Data': data,
            'Timeout': (campaign.originate_timeout if campaign else self.env[
                'asterisk_common.settings'].get_param('originate_timeout')) * 1000,
        })

    @api.model
    def originate_response(self, event):
        # Comes after Hangup the delay so we can handle the situation where
        # no channel was created in Asterisk and no Hangup messages will come.
        logger.info('OriginateResponse: %s', event)
        if event['Response'] != 'Failure':
            logger.error('UNEXPECTED ORIGINATE RESPONSE FROM ASTERISK!')
            return False
        channel = self.env['asterisk_dialer.channel'].with_context(
            active_test=False).search([('uniqueid', '=', event['Uniqueid'])])
        if not channel:
            logger.error('CHANNEL NOT FOUND FOR ORIGINATE RESPONSE')
            return False
        if not channel.campaign:
            logger.warning('CHANNEL DOES NOT BELONG TO CAMPAIGN')
            return False
        if not channel.contact:
            logger.error('CONTACT NOT FOUND FOR CHANNEL %s', event['Channel'])
            return False
        if channel.cause:
            # This is a response afther Hangup so no need for it.
            return True
        channel.write({
            'active': False,
            'cause': event['Reason'],  # 0
            'cause_txt': event['Response'],  # Failure
        })
        if channel.contact:
            channel.contact.write({'state': 'f'})
        self.env.cr.commit()
        channel.campaign.wakeup()
        return True

    @api.model
    def hangup_channel(self, event):
        logger.info('Hangup channel: %s', event)
        # Agent's RPC
        uniqueid = event.get('Uniqueid')
        channel = event.get('Channel')
        found = self.env['asterisk_dialer.channel'].with_context(
            active_test=False).search([('uniqueid', '=', uniqueid)])
        if not found:
            logger.warning('Channel {} not found for hangup.'.format(uniqueid))
            return False
        if not (found.campaign or found.operator or found.contact):
            logger.warning('CHANNEL DOES NOT BELONG TO CAMPAIGN')
            return False
        logger.info('Found %s channel(s) %s', len(found), channel)
        found.write({
            'active': False,
            'end_time': fields.Datetime.now(),
            'cause': event['Cause'],
            'cause_txt': event['Cause-txt'],
        })
        if found.contact:
            if event['Cause'] == '16':
                # Normal call clearing.
                found.contact.write({'state': 'd'})
            else:
                found.contact.write({'state': 'f'})
        self.env.cr.commit()
        if found.campaign:
            found.campaign.wakeup()
        # Delete individual sound file
        if found.contact and found.campaign:
            if found.contact.campaign.campaign_type == 'voice_message' and not found.campaign.tts_is_common:
                filename = 'dialer_campaign_{}_contact_{}.wav'.format(
                    found.campaign.id, found.contact.id)
                self.env.user.asterisk_agent.request(
                    'asterisk.delete_prompt',
                    filename
                )

        return True
