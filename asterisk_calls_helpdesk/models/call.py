# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import json
import logging
from odoo import models, fields, api, _

logger = logging.getLogger(__name__)


class HelpdeskCall(models.Model):
    _name = 'asterisk_calls.call'
    _inherit = 'asterisk_calls.call'

    ticket = fields.Many2one('helpdesk.ticket',
                             ondelete='set null', string='Ticket')

    def create_ticket(self):
        self.ensure_one()
        return {
            'res_model': 'helpdesk.ticket',
            'name': _('Create Ticket'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env['ir.model.data'].xmlid_to_res_id(
                'helpdesk.helpdesk_ticket_view_form'),
            'context': {
                'default_name': self.partner.name if self.partner else self.clid,
                'default_partner_id': self.partner.id if self.partner else False,
                'create_call_ticket': self.id,
            },
        }

    @api.model
    def update_cdr_values(self, original_vals):
        vals = super(
            HelpdeskCall, self).update_cdr_values(original_vals)
        # Check if it is orginated call
        originate_data = self.env['kv_cache.cache'].get(
            original_vals.get('uniqueid'), tag='originated_call',
            serialize='json')
        if not originate_data:
            originate_data = self.env['kv_cache.cache'].get(
                original_vals.get('linkedid'), tag='originated_call',
                serialize='json')
            if originate_data:
                logger.debug(
                    'CDR FOUND TICKET ORIGINATED CALL DATA FROM LINKEDID.')
        model = originate_data.get('model')
        res_id = originate_data.get('res_id')
        if model == 'helpdesk.ticket' and res_id:
            logger.debug('CDR FOUND TICKET FROM ORIGINATED CALL DATA.')
            vals.update({'ticket': res_id})
        elif vals.get('partner'):
            # There is a matched partner so let check if there is open tickets for him.
            # Get closing stages
            open_stages_ids = [k.id for k in self.env['helpdesk.stage'].search(
                [('is_close', '=', False)])]
            open_tickets = self.env['helpdesk.ticket'].search([
                ('partner_id', '=', vals['partner']),
                ('stage_id', 'in', open_stages_ids),
            ])
            if open_tickets:
                # Take the first open ticket
                vals['ticket'] = open_tickets[0].id
        return vals
