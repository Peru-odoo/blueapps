from odoo import fields, models, api

class utmCampaign(models.Model):
    _inherit = "utm.campaign"
    #    _name = 'utm.campaign'
    #    _description = 'Campanhas Segline'
    codigo = fields.Char("Código")
    Situacao = fields.Boolean(
        string='Situação',
        required=False,
        default=1)
    DataInicio = fields.Datetime(
        string='Data de Inicio',
        required=False)
    DataFim = fields.Datetime(
        string='Data Final',
        required=False)
    Obs = fields.Char(
        string='Observação',
        required=False)
    Cidade = fields.Char(
        string='Cidade',
        required=False)
    ocorrencia = fields.Char(
        string='Ocorrencia',
        required=False)
