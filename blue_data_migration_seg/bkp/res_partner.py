# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    name_ar = fields.Char(string="Arabic Name", required=False)
    vend_old_id = fields.Integer(string="Old ID", required=False)
    cust_old_id = fields.Integer(string="Old ID", required=False)
