from odoo import fields, models, api

class Matricula(models.Model):
    _name = 'consignado.matricula'
    _description = 'Informações de matricula e beneficios dos leads.'

    name = fields.Char("Matrícula/NB")
    senha = fields.Char(
        string='Senha',
        tracking=True,
        required=False)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        ondelete="cascade",
        tracking=True,
        required=False)
    cpf_fisica = fields.Char(
        string='CPF',
        tracking=True,
        required=False)
    fisica_rg = fields.Char(
        string='RG',
        tracking=True,
        required=False)
    banco = fields.Char(
        string='Banco',
        required=False)
    agencia = fields.Char(
        string='Agência',
        required=False)
    conta = fields.Char(
        string='Conta',
        required=False)
    tipo_conta = fields.Selection(
        string='Tipo de Conta',
        selection=[('1', 'Corrente'),
                   ('2', 'Poupança')],
        required=False,
        default='1')
    margem_negativa = fields.Float(
        string='Margem Negativa',
        required=False)
    margem_livre = fields.Float(
        string='Margem Livre',
        required=False)
    margem_real = fields.Float(
        string='Margem Real',
        required=False)
    sigla = fields.Char(
        string='Sigla',
        required=False)
    secretaria = fields.Char(
        string='Secretaria',
        required=False)
