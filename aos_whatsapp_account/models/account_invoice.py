# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, sql_db, _
from odoo.tools.mimetypes import guess_mimetype
import requests
import json
import base64
from datetime import datetime
import time
import html2text
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_link(self):
        for inv in self:
            base_url = inv.get_base_url()
            share_url = inv._get_share_url(redirect=True, signup_partner=True)
            url = base_url + share_url
            return url
        
    #@api.multi
    def _get_whatsapp_server(self):
        WhatsappServer = self.env['ir.whatsapp_server']
        whatsapp_ids = WhatsappServer.search([('status','=','authenticated')], order='sequence asc')
        if len(whatsapp_ids) == 1:
            return whatsapp_ids
        return False
            
    #@api.multi
    def send_whatsapp_automatic(self):
        for inv in self:
            new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
            MailMessage = self.env['mail.message']
            WhatsappComposeMessage = self.env['whatsapp.compose.message']
            if inv.payment_state == 'paid':
                template_id = self.env.ref('aos_whatsapp_account.invoice_paid_status', raise_if_not_found=False)
            else:
                template_id = self.env.ref('aos_whatsapp_account.invoice_outstanding_status', raise_if_not_found=False)
            if self._get_whatsapp_server() and self._get_whatsapp_server().status == 'authenticated':
                KlikApi = self._get_whatsapp_server().klikapi()      
                KlikApi.auth()          
                template = template_id.generate_email(inv.id, ['body_html'])
                body = template.get('body_html')
                subject = template.get('subject')
                try:
                    body = body.replace('_PARTNER_', inv.partner_id.name)
                except:
                    _logger.warning('Failed to send Message to WhatsApp number %s', inv.partner_id.whatsapp)
                attachment_ids = []
                chatIDs = []
                message_data = {}
                send_message = {}
                status = 'error'
                partners = self.env['res.partner']          
                if inv.partner_id:
                    partners = inv.partner_id
                    if inv.partner_id.child_ids:
                        #ADDED CHILD FROM PARTNER
                        for partner in inv.partner_id.child_ids:
                            partners += partner
                for partner in partners:
                    if partner.country_id and partner.whatsapp:
                        #SEND MESSAGE
                        whatsapp = partner._formatting_mobile_number()
                        message_data = {
                            'phone': whatsapp,
                            'body': html2text.html2text(body) + inv.get_link(),
                        }
                        if partner.chat_id:
                            message_data.update({'chatId': partner.chat_id, 'phone': ''})
                        data_message = json.dumps(message_data)
                        send_message = KlikApi.post_request(method='sendMessage', data=data_message)
                        if send_message.get('message')['sent']:
                            chatID = send_message.get('chatID')
                            status = 'send'
                            partner.chat_id = chatID
                            chatIDs.append(chatID)
                            _logger.warning('Success to send Message to WhatsApp number %s', whatsapp)
                        else:
                            status = 'error'
                            _logger.warning('Failed to send Message to WhatsApp number %s', whatsapp)
                        new_cr.commit()
                        #time.sleep(3)                
                AllchatIDs = ';'.join(chatIDs)
                vals = WhatsappComposeMessage._prepare_mail_message(self.env.user.partner_id.id, AllchatIDs, inv and inv.id,  'account.move', body, message_data, subject, partners.ids, attachment_ids, send_message, status)
                #vals = WhatsappComposeMessage._prepare_mail_message(self.env.user.partner_id.id, AllchatIDs, [inv.id], 'account.invoice', body, message_data, subject, partners.ids, attachment_ids, send_message, status)
                MailMessage.sudo().create(vals)
                new_cr.commit()
                #time.sleep(3)
                            
