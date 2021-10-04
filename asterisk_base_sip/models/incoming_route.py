# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
from odoo import fields, models, api, _

# TO DELETE

class IncomingRoute(models.Model):
    _name = 'asterisk_base_sip.incoming_route'
    _description = "Incoming route"

    name = fields.Char(required=True)
