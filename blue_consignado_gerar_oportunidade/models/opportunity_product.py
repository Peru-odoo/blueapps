from odoo import api, fields, models, _
import odoo
from odoo.exceptions import UserError

class CrmLeadProduct(models.Model):
    _name = 'crm.lead.product'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        ondelete="cascade",
        required=False)
    matricula_id = fields.Many2one(
        comodel_name='res.partner.benefit',
        string='Matricula',
        ondelete="cascade",
        required=False)
    contrato_id =  fields.Many2one(
        comodel_name='res.partner.contract',
        string='Contrato')
    product_id =  fields.Many2one(
        comodel_name='product.product',
        string='Operação')
    description = fields.Text(string='Descrição')
    qty = fields.Float(string='Quantidade',default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unidade')
    price_unit = fields.Float(string='Consultoria')
    tax_id = fields.Many2many('account.tax', string='Taxas')
    lead_id = fields.Many2one('crm.lead')
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.price_unit = self.product_id.lst_price
            self.product_uom = self.product_id.uom_id.id
            self.tax_id = self.product_id.taxes_id.ids