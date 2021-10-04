from odoo import api, fields, models, _
import odoo
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    proposta = fields.Selection(string='Proposta de Crédito', selection=[('compra de divida','Compra de Divida'),('refinanciamento','Refinanciamento'),('portabilidade','Portabilidade'),('margem','Margem')])
    banco_id = fields.Many2one(
        'res.bank',
        string='Banco Contrato')
    n_contrato = fields.Char(string="Nº do Contrato")
    prazo = fields.Char(string='Prazo/Pagas/Aberto')
    v_parcela = fields.Float(string="Valor da Parcela")
    s_devedor = fields.Float(string="Saldo Devedor")
    t_investimento = fields.Float(string="Taxa Investimento")
    nova_consultoria = fields.Float(string='Nova Consultoria')
    v_liquido = fields.Float(string='Valor Líquido Cliente')
    observacao_cliente = fields.Char(string='Observação do Cliente')
# Novo Contrato
    novo_banco = fields.Text(string='Banco')
    novo_prazo = fields.Char(string='Prazo')
    novo_v_parcela = fields.Float(string='Valor da Parcela')
    v_liquido_geral = fields.Float(string='Valor Líquido Geral')
    v_solicitado = fields.Float(string='Valor Solicitado')
# Matricula
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
    
    
    
    