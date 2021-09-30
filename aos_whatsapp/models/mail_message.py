# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, sql_db, api
from odoo.exceptions import Warning, UserError
from datetime import datetime
import html2text
import threading
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'
    
    message_type = fields.Selection(selection_add=[('whatsapp', 'Whatsapp')],
        ondelete={'whatsapp': lambda recs: recs.write({'message_type': 'email', 'active': False})})    
    whatsapp_server_id = fields.Many2one('ir.whatsapp_server', string='Whatsapp Server')
    whatsapp_status = fields.Selection([('error', 'Error'), ('send', 'Sent')], default='error', string='Status', readonly=True)
    whatsapp_response = fields.Text('Response', readonly=True)
    whatsapp_data = fields.Text('Data', readonly=False)
    whatsapp_chat_id = fields.Char(string='ChatId')
    
    @api.model
    def _resend_whatsapp_message_resend(self, KlikApi):
        try:
            new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
            uid, context = self.env.uid, self.env.context
            with api.Environment.manage():
                self.env = api.Environment(new_cr, uid, context)
                MailMessage = self.env['mail.message'].search([('message_type','=','whatsapp'),('whatsapp_status', '=', 'error')])
                for mail in MailMessage:
                    #data_message = json.dumps(mail.whatsapp_data)
                    message_data = {
                        'chatId': mail.whatsapp_chat_id,
                        'body': html2text.html2text(mail.body),
                    }
                    data_message = json.dumps(message_data)
                    #data_message = html2text.html2text(mail.body)
                    #html2text.html2text(res_id_values.pop('body_html', ''))
                    send_message = KlikApi.post_request(method='sendMessage', data=data_message)
                    #print ('---send_message--',send_message,data_message)
                    if send_message.get('message')['sent']:
                        mail.whatsapp_status = 'send'
                        mail.whatsapp_response = send_message
                        _logger.warning('Success resend Message to WhatsApp number %s', mail.whatsapp_chat_id)
                    else:
                        mail.whatsapp_status = 'error'
                        _logger.warning('Failed resend Message to WhatsApp number %s', mail.whatsapp_chat_id)
                    new_cr.commit()
        finally:
            self.env.cr.close()

    @api.model
    def resend_whatsapp_mail_message(self):
        """Resend whatsapp error message via threding.""" 
        WhatsappServer = self.env['ir.whatsapp_server']
        whatsapp_ids = WhatsappServer.search([('status','=','authenticated')], order='sequence asc')
        if len(whatsapp_ids) == 1:
            if whatsapp_ids.status != 'authenticated':
                _logger.warning('Whatsapp Authentication Failed!\nConfigure Whatsapp Configuration in Whatsapp Server.')
            KlikApi = whatsapp_ids.klikapi()
            KlikApi.auth()
            thread_start = threading.Thread(target=self._resend_whatsapp_message_resend(KlikApi))
            thread_start.start()
        return True