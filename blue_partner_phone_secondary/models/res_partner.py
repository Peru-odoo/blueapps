# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    id_segline = fields.Char(string="ID/CPF", required=False)

    ddD1 = fields.Char(string="DDD1")
    telefone1 = fields.Char(string="Telefone 1")
    ddD2 = fields.Char(string="DDD2")
    telefone2 = fields.Char(string="Telefone 2")
    ddD3 = fields.Char(string="DDD3")
    telefone3 = fields.Char(string="Telefone 3")
    ddD4 = fields.Char(string="DDD4")
    telefone4 = fields.Char(string="Telefone 4")
    ddD5 = fields.Char(string="DDD5")
    telefone5 = fields.Char(string="Telefone 5")
    ddD6 = fields.Char(string="DDD6")
    telefone6 = fields.Char(string="Telefone 6")
    ddD7 = fields.Char(string="DDD7")
    telefone7 = fields.Char(string="Telefone 7")
    ddD8 = fields.Char(string="DDD8")
    telefone8 = fields.Char(string="Telefone 8")
    ddD9 = fields.Char(string="DDD9")
    telefone9 = fields.Char(string="Telefone 9")
    ddD10 = fields.Char(string="DDD10")
    telefone10 = fields.Char(string="Telefone 10")
