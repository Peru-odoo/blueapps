# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

import urllib3
import json



class ResPartner(models.Model):
    _inherit = "res.partner"

    phone2 = fields.Char("Phone (Secondary)")
    ddD1 = fields.Char("DDD1")
    telefone1 = fields.Char("Telefone 1")
    ddD2 = fields.Char("DDD2")
    telefone2 = fields.Char("Telefone 2")
    ddD3 = fields.Char("DDD3")
    telefone3 = fields.Char("Telefone 3")
    ddD4 = fields.Char("DDD4")
    telefone4 = fields.Char("Telefone 4")
    ddD5 = fields.Char("DDD5")
    telefone5 = fields.Char("Telefone 5")
    ddD6 = fields.Char("DDD6")
    telefone6 = fields.Char("Telefone 6")
    ddD7 = fields.Char("DDD7")
    telefone7 = fields.Char("Telefone 7")
    ddD8 = fields.Char("DDD8")
    telefone8 = fields.Char("Telefone 8")     
    ddD9 = fields.Char("DDD9")
    telefone9 = fields.Char("Telefone 9")   
    ddD10 = fields.Char("DDD10")
    telefone10 = fields.Char("Telefone 10") 
    campanha = fields.Char("Campanha")
    nomeCampanha = fields.Char("Nome da Campanha")
    beneficio1 = fields.Char("Beneficio 1")
    beneficio1 = fields.Char("Beneficio 2")
    agbcocred = fields.Char("Agencia")
    ccbcocred = fields.Char("Conta")
    datanasc = fields.Char("Nascimento")

    @api.onchange("phone2", "country_id", "company_id")
    def _onchange_phone2_validation(self):
        # Compatibility with phone_validation
        if hasattr(self, "phone_format"):
            if self.phone2:
                self.phone2 = self.phone_format(self.phone2)
