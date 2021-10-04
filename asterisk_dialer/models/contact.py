# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import models, fields, api, _

logger = logging.getLogger(__name__)


STATE_LIST = [
    ('q', _('Queued')),
    ('p', _('In Progress')),
    ('c', _('Connected')),
    ('d', _('Done')),
    ('f', _('Failed')),
]

MODELS = [
    ('res.partner', _('Partners')),
]


class Contact(models.Model):
    _name = 'asterisk_dialer.contact'
    _rec_name = 'phone'
    _description = 'Contact'

    campaign = fields.Many2one(
        'asterisk_dialer.campaign', ondelete='cascade',
        required=True, index=True,
        default=lambda self: self.env['asterisk_common.settings'].get_param('default_campaign')
    )
    phone = fields.Char(
        required=True, index=True, size=15,
        help=_("Phone number.")
    )
    state = fields.Selection(STATE_LIST, required=True,
                             index=True, default='q')
    name = fields.Char(
        compute='_compute_name', inverse='_set_name', store=True,
        help=_("A descriptive name for the contact.")
    )

    description = fields.Text()
    model = fields.Char(compute='_compute_model', string='Model',
                             store=True)
    model_object = fields.Reference(MODELS, readonly=True)
    contact_name = fields.Char()
    calls = fields.One2many(
        'asterisk_dialer.channel', 'contact', context={'active_test': False},
        help=_("Call history for this contact.")
    )
    dial_attempt = fields.Integer(default=0)
    notes = fields.One2many(
        'asterisk_dialer.contact_note', 'contact',
        help=_("Add notes about the contact here.")
    )
    active = fields.Boolean(default=True, index=True)


    _sql_constraints = [
        ('phone_campaign_unique',
         'unique (phone,campaign)',
         _('This phone already exists in this campaign!'))
    ]

    @api.depends('contact_name', 'model_object')
    def _compute_name(self):
        for rec in self:
            if rec.model_object:
                rec.name = rec.model_object.name
            else:
                rec.name = rec.contact_name

    def _set_name(self):
        for rec in self:
            if rec.model_object:
                rec.model_object.name = rec.name
            else:
                rec.contact_name = rec.name

    @api.depends('model_object')
    def _compute_model(self):
        for rec in self:
            if rec.model_object:
                rec.model = rec.model_object._name
            else:
                rec.model = self._name

    @api.onchange('state')
    def _reset_dial_attempt(self):
        for rec in self:
            if rec.state == 'q':
                rec.dial_attempt = 0

    def write(self, vals):
        for rec in self:
            rec.campaign.log(content=[rec, vals, ['state']], level='debug')
        res = super(Contact, self).write(vals)
        return res

    def originate(self):
        self.env['asterisk_dialer.channel'].originate(
            channel=self.campaign.channel_provider.replace(
                '{NUMBER}', self.phone),
            app='AGI',
            data='agi:async',
            campaign=self.campaign,
            contact=self,
        )
