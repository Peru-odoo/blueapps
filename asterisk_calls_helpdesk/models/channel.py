# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import json
import logging
from odoo import models, fields, api, _

logger = logging.getLogger(__name__)


class HelpdeskChannel(models.Model):
    _name = 'asterisk_calls.channel'
    _inherit = 'asterisk_calls.channel'

    ticket = fields.Many2one(
        'helpdesk.ticket', ondelete='set null', string='Helpdesk')

    def open_ticket(self):
        self.ensure_one()
        return {
            'res_model': 'helpdesk.ticket',
            'res_id': self.ticket.id,
            'name': _('Create Ticket'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env['ir.model.data'].xmlid_to_res_id(
                'helpdesk.helpdesk_ticket_view_form'),
        }

    @api.model
    def update_channel_values(self, original_vals):
        vals = super(
            HelpdeskChannel, self).update_channel_values(original_vals)
        # Check if it is orginated call
        originate_data = self.env['kv_cache.cache'].get(
            original_vals.get('uniqueid'), tag='originated_call',
            serialize='json')
        if not originate_data:
            originate_data = self.env['kv_cache.cache'].get(
                original_vals.get('linkedid'), tag='originated_call',
                serialize='json')
            if originate_data:
                logger.debug('FOUND TICKET ORIGINATED CALL DATA FROM LINKEDID.')
        model = originate_data.get('model')
        res_id = originate_data.get('res_id')
        if model == 'helpdesk.ticket' and res_id:
            logger.debug('FOUND TICKET FROM ORIGINATED CALL DATA.')
            vals.update({'ticket': res_id})
        elif vals.get('partner'):
            # There is a matched partner so let check if there is open tickets for him.
            # Get closing stages
            open_stages_ids = [k.id for k in self.env['helpdesk.stage'].search(
                [('is_close', '=', False)])]
            open_tickets = self.env['helpdesk.ticket'].search([
                ('partner_id', '=', vals['partner']),
                ('stage_id', 'in', open_stages_ids),
            ], order='id desc')
            if len(open_tickets) > 1:
                logger.warning('MULTIPLE TICKETS FOUND FOR CALLER')
            if open_tickets:
                # Take the first open ticket
                vals['ticket'] = open_tickets[0].id
        return vals

    def reload_channels(self, data={}):
        if self.ticket:
            return super(HelpdeskChannel, self).reload_channels(
                data=dict(res_id=self.ticket.id, model='helpdesk.ticket'))
        else:
            return super(HelpdeskChannel, self).reload_channels(data=data)

