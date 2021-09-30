from odoo import api, fields, models, _
import odoo
from odoo.exceptions import UserError

class CrmLeadProduct(models.Model):
    _name = 'crm.lead.product'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        ondelete="cascade",
        required=True)
    matricula_id = fields.Many2one(
        comodel_name='res.partner.benefit',
        string='Matricula',
        ondelete="cascade",
        required=True)
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

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    matricula_id = fields.Many2one(
        string="Matricula",
        required="True",
        comodel_name="res.partner.benefit",
        domain="[('partner_id', '=', partner_id)]",
#        context={"key": "value"},
        ondelete="cascade",
        copy=True,
        help="Seleciona a matricula qual deseja inserir no negocio.",
    )
    lead_product_ids = fields.One2many('crm.lead.product','lead_id',string='Contratos para Negociar')

    def action_create_quotation(self):
        sale_obj=self.env['sale.order']
        sale_line_obj=self.env['sale.order.line']
        order_lines = []
        for line in self.lead_product_ids:
            order_lines.append((0,0,{'product_id': line.product_id.id,
                'name': line.description,
                'product_uom_qty':line.qty,
                'price_unit': line.price_unit,
                'tax_id':[(6, 0, line.tax_id.ids)]

            }))
        if self.partner_id:
            sale_id = sale_obj.create({
                'partner_id':self.partner_id.id,
                'team_id': self.team_id.id,
                'campaign_id': self.campaign_id.id,
                'medium_id': self.medium_id.id,
                'source_id': self.source_id.id,
                'opportunity_id': self.id,
                'order_line':order_lines,
            })
        else:
            raise UserError('Para gerar uma ficha cadastral, o campo de cliente não deve estar vazio!!!')
        return True
    
    
    
    