# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from phonenumbers import phonenumberutil
import phonenumbers
from odoo import api, models, tools, fields, release, _
from odoo.exceptions import ValidationError, UserError

logger = logging.getLogger(__name__)


class Ticket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = 'helpdesk.ticket'

    asterisk_calls_count = fields.Integer(compute='_get_asterisk_calls_count',
                                          string=_('Calls'))
    partner_phone = fields.Char(related='partner_id.phone')
    partner_mobile = fields.Char(related='partner_id.mobile')

    def _get_asterisk_calls_count(self):
        for rec in self:
            rec.asterisk_calls_count = self.env[
                'asterisk_calls.call'].search_count([('ticket', '=', rec.id)])

    @api.model
    def create(self, vals):
        res = super(Ticket, self).create(vals)
        try:
            if self.env.context.get('create_call_ticket'):
                call = self.env['asterisk_calls.call'].browse(
                    self.env.context['create_call_ticket'])
                call.ticket = res.id
        except Exception as e:
            logger.exception(e)
        return res
