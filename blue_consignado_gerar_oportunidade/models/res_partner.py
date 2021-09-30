from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    fisica_cpf = fields.Char(
        string='CPF',
        required=False)

    fisica_rg = fields.Char(
        string='RG',
        required=False)
        
    contratos = fields.Text(
        string='Todos Contratos',
        required=False)

    beneficios = fields.Text(
        string='Todas Matriculas/NB',
        required=False)

    beneficio1 = fields.Char(
        string='Matricula/NB 1',
        required=False)

    beneficio2 = fields.Char(
        string='Matricula/NB 2',
        required=False)

    beneficio3 = fields.Char(
        string='Matricula/NB 3',
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

    matricula_id = fields.Many2one(
        string="Matricula",
        required=False,
        comodel_name="res.partner.benefit",
#        domain="[('partner_id', '=', partner_id)]",
#        context={"key": "value"},
        ondelete="cascade",
        copy=True,
        help="Seleciona a matricula qual deseja inserir no negocio.")  

    matricula_ids = fields.One2many(
        comodel_name='res.partner.benefit',
        inverse_name='partner_id',
        string='Matriculas',
        track_visibility='onchange',
        required=False)

    contrato_ids = fields.One2many(
        comodel_name='res.partner.contract',
        inverse_name='partner_id',
        string='Contratos',
        track_visibility='onchange',
        required=False)



