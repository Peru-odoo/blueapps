# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    id_segline = fields.Integer(string="ID Segline", required=False)
    phone2 = fields.Integer(string="Phone (Secondary)")
    ddD1 = fields.Integer(string="DDD1")
    telefone1 = fields.Integer(string="Telefone 1")
    ddD2 = fields.Integer(string="DDD2")
    telefone2 = fields.Integer(string="Telefone 2")
    ddD3 = fields.Integer(string="DDD3")
    telefone3 = fields.Integer(string="Telefone 3")
    ddD4 = fields.Integer(string="DDD4")
    telefone4 = fields.Integer(string="Telefone 4")
    ddD5 = fields.Integer(string="DDD5")
    telefone5 = fields.Integer(string="Telefone 5")
    ddD6 = fields.Integer(string="DDD6")
    telefone6 = fields.Integer(string="Telefone 6")
    ddD7 = fields.Integer(string="DDD7")
    telefone7 = fields.Integer(string="Telefone 7")
    ddD8 = fields.Integer(string="DDD8")
    telefone8 = fields.Integer(string="Telefone 8")
    ddD9 = fields.Integer(string="DDD9")
    telefone9 = fields.Integer(string="Telefone 9")
    ddD10 = fields.Integer(string="DDD10")
    telefone10 = fields.Integer(string="Telefone 10")
    campanha = fields.Char(string="Campanha")
    nomeCampanha = fields.Char(string="Nome da Campanha")
    beneficio1 = fields.Char(string="Beneficio 1")
    beneficio1 = fields.Char(string="Beneficio 2")
    agbcocred = fields.Char(string="Agencia")
    ccbcocred = fields.Char(string="Conta")
    datanasc = fields.Char(string="Nascimento")

    @api.onchange("phone2", "country_id", "company_id")
    def _onchange_phone2_validation(self):
        # Compatibility with phone_validation
        if hasattr(self, "phone_format"):
            if self.phone2:
                self.phone2 = self.phone_format(self.phone2)
