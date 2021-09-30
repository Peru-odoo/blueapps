# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields,tools, models,_
from odoo.exceptions import ValidationError

class Customer(models.TransientModel):
    _name = 'customer.wizard'
    _description = 'Customer'

    filter_id = fields.Many2one('quotation.saleorder',string="Filter")
    salespersons_ids = fields.Many2many("res.users",string="Salespersons")
    product_ids = fields.Many2many("product.product",string="Product")
    product_not_set_ids = fields.Many2many("product.product",'product_id',string="Products Not Set")
    sale_team_ids = fields.Many2many("crm.team",string="Sales Team")
    sale_team_not_set_ids = fields.Many2many("crm.team",'team_id',string="Sales Team Not Set")
    save_filter = fields.Boolean(string="Save Filter")
    filter_name = fields.Char(string="Filter Name")

    def set_quotation(self):
        if self.salespersons_ids.ids or self.product_ids.ids or self.product_not_set_ids.ids or self.sale_team_ids.ids or self.sale_team_not_set_ids.ids:
            domain = self.domain_all()
            domain.append(('state','=','draft'))
            return {
                'type': 'ir.actions.act_window',
                'name': 'Quotation',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'domain': domain,
                 }
        else:
            raise ValidationError('Data not found!')

    def domain_all(self):
        customer_obj = self.env['res.partner'].search([('user_id','in',self.salespersons_ids.ids)])
        product_obj = self.env['sale.order.line'].search([('product_id','in',self.product_ids.ids)])
        product_not_set_obj = self.env['sale.order.line'].search([('product_id','in',self.product_not_set_ids.ids)])
        sale_team_obj = self.env['crm.team'].search([('id','in',self.sale_team_ids.ids)])
        sale_team_not_set_obj = self.env['crm.team'].search([('id','in',self.sale_team_not_set_ids.ids)])
        domain = []
        ls_sale_team_not_set = []
        for saleteamnotset in sale_team_not_set_obj:
            if saleteamnotset:
                ls_sale_team_not_set.append(saleteamnotset.id)
        if ls_sale_team_not_set:
            domain.append(('team_id','not in',ls_sale_team_not_set))

        ls_sale_team = []
        for saleteam in sale_team_obj:
            if saleteam:
               ls_sale_team.append(saleteam.id)
        if ls_sale_team:
            domain.append(('team_id','in',ls_sale_team)) 

        ls_product_not_set = []
        for saleorder in product_not_set_obj:
            if saleorder:
                ls_product_not_set.append(saleorder.id)
        if ls_product_not_set:
            domain.append(('order_line','not in',ls_product_not_set))

        ls_product = []
        for line in product_obj:
            if line:
                ls_product.append(line.id)
        if ls_product:
            domain.append(('order_line','in',ls_product))
        elif self.product_ids.ids:
            domain.append(('order_line','in',self.product_ids.ids))

        ls = []
        for record in customer_obj:
            if record:
                ls.append(record.id)
        if ls:
            domain.append(('partner_id','in',ls))
        elif self.salespersons_ids.ids:
            domain.append(('partner_id','=',False))

        return domain

    def set_sale_order(self):
        if self.salespersons_ids.ids or self.product_ids.ids or self.product_not_set_ids.ids or self.sale_team_ids.ids or self.sale_team_not_set_ids.ids:
            domain = self.domain_all()
            domain.append(('state','=','sale'))
            return {
                'type': 'ir.actions.act_window',
                'name': 'Quotation',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'domain': domain,
                 }
        else:
            raise ValidationError('Data not found!')

    def set_quotation_sale_order(self):
        if self.salespersons_ids.ids or self.product_ids.ids or self.product_not_set_ids.ids or self.sale_team_ids.ids or self.sale_team_not_set_ids.ids:
            domain = self.domain_all()
            return {
                'type': 'ir.actions.act_window',
                'name': 'Quotation',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'domain': domain,
                 }
        else:
            raise ValidationError('Data not found!')

    def save_filter_quotation(self):
        filter_dict = {'name':self.filter_name,
                       'salespersons_ids':self.salespersons_ids.ids,
                       'product_ids':self.product_ids.ids,
                       'product_not_set_ids':self.product_not_set_ids.ids,
                       'sale_team_ids':self.sale_team_ids.ids,
                       'sale_team_not_set_ids':self.sale_team_not_set_ids.ids
                       }
        filter_obj = self.env['quotation.saleorder'].create(filter_dict)

    @api.onchange('filter_id')
    def onchange_filter_id(self):
        if self.filter_id:
            if self.filter_id.salespersons_ids.ids:
                self.salespersons_ids = self.filter_id.salespersons_ids.ids
            else:
                self.salespersons_ids = False
            if self.filter_id.product_ids.ids:
                self.product_ids = self.filter_id.product_ids.ids
            else:
                self.product_ids = False
            if self.filter_id.product_not_set_ids.ids:
                self.product_not_set_ids = self.filter_id.product_not_set_ids.ids
            else:
                self.product_not_set_ids = False
            if self.filter_id.sale_team_ids.ids:
                self.sale_team_ids = self.filter_id.sale_team_ids.ids
            else:
                self.sale_team_ids = False
            if self.filter_id.sale_team_not_set_ids.ids:
                self.sale_team_not_set_ids = self.filter_id.sale_team_not_set_ids.ids  
            else:
                self.sale_team_not_set_ids = False
