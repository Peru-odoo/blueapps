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

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    lead_product_ids = fields.One2many('res.partner.contract','partner_id',string='Contratos à Negociar')

    def action_create_lead(self):
        sale_obj=self.env['crm.lead']
        sale_line_obj=self.env['res.partner.contract']
        order_lines = []
        for line in self.contrato_ids:
            order_lines.append((0,0,{'matricula_id': line.matricula_id.id,
                'name': line.partner_id.name,
                'contrato_id':line.id
#                'price_unit': line.price_unit,
#                'tax_id':[(6, 0, line.tax_id.ids)]

            }))
        if self.id:
            lead_id = sale_obj.create({
                'partner_id':self.id,
#                'team_id': self.team_id.id,
#                'campaign_id': self.campaign_id.id,
#                'medium_id': self.medium_id.id,
#                'source_id': self.source_id.id,
#                'opportunity_id': self.id,
                'lead_product_ids':order_lines,
            })
        else:
            raise UserError('In order to create sale order, Customer field should not be empty !!!')
        return True
    
    
    
    