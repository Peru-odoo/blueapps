# -*- coding: utf-8 -*-
from odoo import api, fields, models,_

class SaleOrder(models.Model):
    _inherit = "sale.order"

    coste_total = fields.Monetary(compute='_product_margin_total', currency_field='currency_id', store=True,string="Total cost")

    @api.depends('order_line.margin','margin')
    def _product_margin_total(self):
        for order in self:
            order.coste_total = order.amount_untaxed - order.margin
