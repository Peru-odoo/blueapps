# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


class User(models.Model):
    _inherit = 'res.users'
    _description = "Guides"

    web_phone_sip_user = fields.Char(string="SIP User")
    web_phone_sip_secret = fields.Char(string="SIP Secret")
    web_phone_sip_protocol = fields.Char(string="SIP Protocol", default='udp')
    web_phone_sip_proxy = fields.Char(string="SIP Proxy")
    web_phone_websocket = fields.Char(string="Websocket")
    web_phone_stun_server = fields.Char(string="Stun Server", default='stun.l.google.com:19302')

