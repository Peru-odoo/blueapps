from odoo import fields, models, api
from odoo.exceptions import UserError

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
        domain="[('partner_id', '=', id)]",
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
#        lead_product_ids = fields.One2many('res.partner.contract','partner_id',string='Contratos à Negociar')

    def action_create_lead(self):
        sale_obj=self.env['crm.lead']
        sale_line_obj=self.env['crm.lead.product']
#        sale_line_obj=self.env['res.partner.contract']
        order_lines = []
        for line in self.contrato_ids:
            order_lines.append((0,0,{
                'partner_id': line.partner_id.id,
                'matricula_id': line.matricula_id.id,
                'description': line.partner_id.name,
                'contrato_id': line.id
#                'price_unit': line.price_unit,
#                'tax_id':[(6, 0, line.tax_id.ids)]
            }))
        if self.id:
            lead_id = sale_obj.create({
                'name': self.name,
                'partner_id':self.id, 
                'matricula_id': self.matricula_id.id,
#                'contrato_id': self.contrato_id.id,
#                'team_id': self.team_id.id,
#                'campaign_id': self.campaign_id.id,
#                'medium_id': self.medium_id.id,
#                'source_id': self.source_id.id,
#                'opportunity_id': self.id,
                'lead_product_ids':order_lines
            })
        else:
            raise UserError('In order to create sale order, Customer field should not be empty !!!')
        return True


