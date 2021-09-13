from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    fisica_cpf = fields.Char(related='id_segline',
        string='CPF',
        tracking=True,
        required=False)

    fisica_rg = fields.Char(
        string='RG',
        tracking=True,
        required=False)
        
    contratos = fields.Text(
        string='Todos Contratos',
        tracking=True,
        required=False)

    beneficios = fields.Text(
        string='Todas Matriculas/NB',
        tracking=True,
        required=False)

    beneficio1 = fields.Char(
        string='Matricula/NB 1',
        tracking=True,
        required=False)

    beneficio2 = fields.Char(
        string='Matricula/NB 2',
        tracking=True,
        required=False)

    beneficio3 = fields.Char(
        string='Matricula/NB 3',
        tracking=True,
        required=False)

    mae = fields.Char(
        string='Nome da Mãe',
        required=False)

    esp = fields.Char(
        string='Espécie de Benefício',
        required=False)

    descesp = fields.Char(
        string='Descrição do Benefício',
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