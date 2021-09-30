# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
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
from odoo import api, fields, models,_

class QuotationSaleorder(models.Model):
    _name = "quotation.saleorder"
    _description = 'Search Quotation/Sales order'

    name = fields.Char(string="Filter Name",required=True)
    salespersons_ids = fields.Many2many("res.users",string="Salespersons")
    product_ids = fields.Many2many("product.product",string="Product")
    product_not_set_ids = fields.Many2many("product.product",'name',string="Products Not Set")
    sale_team_ids = fields.Many2many("crm.team",string="Sales Team")
    sale_team_not_set_ids = fields.Many2many("crm.team",'id',string="Sales Team Not Set")
