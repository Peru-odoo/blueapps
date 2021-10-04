# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
#-*- encoding: utf-8 -*-
import logging
from odoo import fields, models, api, _

# TO DELETE


class OutgoingRouteGroup(models.Model):
    _name = 'asterisk_base_sip.outgoing_route_group'
    _description = 'Outgoing Route Group'

    name = fields.Char(required=True)
