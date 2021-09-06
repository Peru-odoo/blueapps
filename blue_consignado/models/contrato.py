from odoo import fields, models, api


class Contratos (models.Model):
    _name = 'consignado.contrato'
    _description = 'Contratos à negociar'

    name = fields.Char("N. Contrato",
                       required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        required=True)
    matricula = fields.Many2one(
        comodel_name='consignado.matricula',
        string='Matricula',
        required=True)
    banco_origem = fields.Char(
        string='Banco Origem',
        required=False)
    saldo_devedor = fields.Float(
        string='Saldo Devedor',
        required=False)
    valor_parcela = fields.Float(
        string='Valor Parcela',
        required=False)
    valor_liberado = fields.Float(
        string='Valor Liberado',
        required=False)
    valor_consultoria = fields.Float(
        string='Valor Consultoria',
        required=False)
    valor_liquido = fields.Float(
        string='Valor Liquido',
        required=False)
    qtd_parcelas = fields.Char(
        string='Qtd. Parcelas',
        required=False)



