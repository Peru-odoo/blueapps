from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartnerContract(models.Model):
    _name = 'res.partner.contract'
    _description = 'Informações de matricula e beneficios dos leads.'

    name = fields.Char("N. Contrato",
                       required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        ondelete="cascade",
        required=False)
    matricula_id = fields.Many2one(
        comodel_name='res.partner.benefit',
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
    product_id =  fields.Many2one('product.product',string='Product')
    description = fields.Text(string='Description')
    qty = fields.Float(string='Ordered Qty',default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float(string='Unit Price')
    tax_id = fields.Many2many('account.tax', string='Taxes')
    lead_id = fields.Many2one('crm.lead')
    partner_id = fields.Many2one('res.partner')
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.price_unit = self.product_id.lst_price
            self.product_uom = self.product_id.uom_id.id
            self.tax_id = self.product_id.taxes_id.ids

    
    
    