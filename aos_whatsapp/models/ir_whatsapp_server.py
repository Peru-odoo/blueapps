# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from email import encoders
from email.charset import Charset
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formataddr, formatdate, getaddresses, make_msgid
import logging
import re
import smtplib
import json
import threading
from ..klikapi import KlikApi

import html2text

from odoo import api, fields, models, tools, _, sql_db
from odoo.exceptions import except_orm, UserError
from odoo.tools import ustr, pycompat

_logger = logging.getLogger(__name__)

SMTP_TIMEOUT = 60


class IrWhatsappServer(models.Model):
    """Represents an SMTP server, able to send outgoing emails, with SSL and TLS capabilities."""
    _name = "ir.whatsapp_server"
    _description = 'Whatsapp Server'

    name = fields.Char(string='Description', required=True, index=True)
    sequence = fields.Integer(string='Priority', default=10, help="When no specific mail server is requested for a mail, the highest priority one "
                                                                  "is used. Default priority is 10 (smaller number = higher priority)")
    active = fields.Boolean(default=True)
    klik_key = fields.Char("KlikApi Key", help="Optional key for SMTP authentication")
    klik_secret = fields.Char("KlikApi Secret", help="Optional secret for SMTP authentication")
    qr_scan = fields.Binary("QR Scan")
    status = fields.Selection([('init','Initial Status'),
                               ('loading', 'Loading'),
                               ('got qr code', 'QR Code'),
                               ('authenticated', 'Authenticated')], default='init', string="Status")
    hint = fields.Char(string='Hint', readonly=True, default="Configure Token and Instance")
    message_ids = fields.One2many('mail.message', 'whatsapp_server_id', string="Mail Message")    
    message_counts = fields.Integer('Message Sent Counts', compute='_get_mail_message_whatsapp')
    notes = fields.Text(readonly=True)
    
    def _get_mail_message_whatsapp(self):
        KlikApi = self.klikapi()
        KlikApi.auth()
        data = KlikApi.get_count()
        self.message_counts = data
    
    def _formatting_mobile_number(self, number):
        for rec in self:
            module_rec = self.env['ir.module.module'].sudo().search_count([
                ('name', '=', 'crm_phone_validation'),
                ('state', '=', 'installed')])
            return module_rec and re.sub("[^0-9]", '', number) or \
                str(rec.partner_id.country_id.phone_code
                    ) + number

    def klikapi(self):
        return KlikApi(self.klik_key, self.klik_secret)
    
    def klikapi_status(self):
        #WhatsApp is open on another computer or browser. Click “Use Here” to use WhatsApp in this window.
        data = {}
        KlikApi = self.klikapi()
        KlikApi.auth()
        data = KlikApi.get_request(method='status', data=data)
        # print ('---data---',data)
        if data.get('accountStatus') == 'loading':
            self.hint = 'Auth status is Loading! Please click QR Code/Use here again'
            self.status = 'loading'
            self.notes = ''
        elif data.get('accountStatus') == 'authenticated':
            #ALREADY SCANNED
            self.hint = 'Auth status Authenticated'
            self.status = 'authenticated'
            self.notes = ''
        elif data.get('qrCode'):
            #FIRST SCANNED OR RELOAD QR
            #print('33333')
            qrCode = data.get('qrCode').split(',')[1]
            self.qr_scan = qrCode
            self.status = 'got qr code'
            self.hint = 'To send messages, you have to authorise like for WhatsApp Web'
            self.notes = """1. Open the WhatsApp app on your phone
2. Press Settings->WhatsApp WEB and then plus
3. Scan a code and wait a minute
4. Keep your phone turned on and connected to the Internet
A QR code is valid only for 45 seconds. Message sennding will be available right after authorization."""
        else:
            #print('44444')
            #ERROR GET QR
            self.qr_scan = False
            self.status = 'init'
            self.hint = data.get('error')
            self.notes = ''
    
    def klikapi_logout(self):
        KlikApi = self.klikapi()
        KlikApi.auth()
        KlikApi.logout()
        self.write({'qr_scan': False, 'hint': 'Logout Success', 'notes': '', 'status': 'init'})
        
    
    def redirect_whatsapp_key(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://klikodoo.id/shop/product/whatsapp-api-14',
            'target': '_new',
        }
        
    @api.model
    def _send_whatsapp(self, numbers, message):
        """ Send whatsapp """
        KlikApi = self.klikapi()
        KlikApi.auth()
        new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
        for number in numbers:
            whatsapp = self._formatting_mobile_number(number)
            message_data = {
                'phone': whatsapp,
                'body': html2text.html2text(message),
            }
            data_message = json.dumps(message_data)
            send_message = KlikApi.post_request(method='sendMessage', data=data_message)
            if send_message.get('message')['sent']:
                _logger.warning('Success to send Message to WhatsApp number %s', whatsapp)
            else:
                _logger.warning('Failed to send Message to WhatsApp number %s', whatsapp)
            new_cr.commit()
        return True
