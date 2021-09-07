from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    fisica_cpf = fields.Char(
        string='CPF',
        tracking=True,
        required=False)
    fisica_rg = fields.Char(
        string='RG',
        tracking=True,
        required=False)
    matricula_id = fields.One2many(
        comodel_name='consignado.matricula',
        inverse_name='partner_id',
        string='Matriculas',
        track_visibility='onchange',
        required=False)
    contrato_id = fields.One2many(
        comodel_name='consignado.contrato',
        inverse_name='partner_id',
        string='Contratos',
        track_visibility='onchange',
        required=False)
