# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, sql_db, _
from odoo.tools.mimetypes import guess_mimetype
from datetime import datetime
from odoo.exceptions import UserError
import html2text
import logging

_logger = logging.getLogger(__name__)

class WhatsappComposeMessage(models.TransientModel):
    _inherit = 'whatsapp.compose.message'
    
    invoice_ids = fields.Many2many('account.move', string='Invoice')
    
    @api.model
    def default_get(self, fields):
        result = super(WhatsappComposeMessage, self).default_get(fields)
        if self.env.context.get('active_model') and self.env.context.get('active_id'):
            active_model = self.env.context.get('active_model')
            res_id = self.env.context.get('active_id')
            res_ids = self.env.context.get('active_ids')
            rec = self.env[active_model].browse(res_id)
            msg_invoices = ''
            result['subject'] = ''
            is_multi_invoice = False
            if active_model == 'account.move':
                result['invoice_ids'] = res_ids
                if len(res_ids) > 1:
                    template_id = self.env.ref('aos_whatsapp_account.invoice_overdue_status', raise_if_not_found=False)
                    for inv in self.env[active_model].browse(res_ids):
                        msg_invoices += inv.number + ': ' + self.format_amount(inv.amount_total, inv.currency_id) + "\n"
                    is_multi_invoice = True
                    result['attachment_ids'] = []
                else:
                    template_id = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
            elif active_model == 'account.payment':
                template_id = self.env.ref('account.mail_template_data_payment_receipt', raise_if_not_found=False)
            msg = result.get('message', '')
            if active_model == 'account.move' or active_model == 'account.payment':
                template = template_id.generate_email(rec.id, ['body_html'])
                body = template.get('body_html')
                msg = html2text.html2text(body)
                if not is_multi_invoice:
                    result['template_id'] = template_id and template_id.id
                    result['subject'] = template_id and template_id.subject
                result['subject'] = result['subject'] or 'Invoice Outstanding'
            result['message'] = msg
        return result
    
    #@api.multi
    def send_mail(self):
        vals = self.invoice_ids
        for order in vals:
            email_act = order.action_invoice_sent()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                email_ctx.update(default_email_from=order.company_id.email)
                order.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))  
        return True
                