# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.addons.website.models import ir_http
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = "product.template"    
    
    quote_products = fields.Boolean(string='Request for Quote products')    
    
    _defaults = {
        'quote_products': False
    }

    is_extra_price = fields.Boolean(string='Extra Price',compute = '_compute_extra_price',default=False)

    
    def _compute_extra_price(self):
        
        product_pricelist = self.env['product.pricelist.item']
        p_pricelist = 0.0
        for rec in self:
            # product_pricelist.search([('product_tmpl_id','=',rec.id),('fixed_price','>',)])
            pricelist_item_ids = product_pricelist.search([('fixed_price','>',0)])
            if rec:
                for item in pricelist_item_ids:
                    if item.applied_on == '1_product':
                        p_pricelist = product_pricelist.search_count([('product_tmpl_id','=',rec.id)])
                    elif item.applied_on == '0_product_variant':
                        product_id = self.env['product.product'].search([('product_tmpl_id','=',rec.id)],limit=1).id
                        p_pricelist = product_pricelist.search_count([('product_id','=',product_id)])
                    else:
                        continue
                    if p_pricelist > 0.0:                        
                        rec.is_extra_price = True
                    else:
                        rec.is_extra_price = False
                   





            
   

        
# class ProductProduct(models.Model):
#     _inherit = "product.product"

#     quote_products = fields.Boolean(string='Request for Quote products')

class Website(models.Model):
    _inherit = 'website'


    def get_quote_products(self):   
        quote_ids=self.env['product.template'].sudo().search([('quote_products','=','True')])
        
        return quote_ids  

    def get_qty(self):
        res = 0
        if request.session['uid']:
            quote_cart_ids = self.env['quote.order'].sudo().search([('partner_id','=',self.env.user.partner_id.id)])
            request.session['quote_order_id'] = quote_cart_ids.id
        else:
            if 'quote_order_id' in request.session.keys():
                quote_cart_ids = self.env['quote.order'].sudo().browse(request.session['quote_order_id'])
            else:
                quote_cart_ids = self.env['quote.order'].sudo().browse(None)
        
        for i in quote_cart_ids.quote_lines:
            res = res +i.qty
        return int(res)

    
    def get_quote_cart_products(self):
        if request.session['uid']:
            quote_cart_ids = self.env['quote.order'].sudo().search([('partner_id','=',self.env.user.partner_id.id)])
            request.session['quote_order_id'] = quote_cart_ids.id
        # order =  self.env['quote.order'].sudo().search([])    
        if 'quote_order_id' in request.session.keys():          
            quote_cart_ids = self.env['quote.order'].sudo().browse(request.session['quote_order_id'])       
            return quote_cart_ids.quote_lines           

class QuoteOrderLine(models.Model):

    _name = 'quote.order.line'
    _description = "Quote Order Line"
    
    product_id = fields.Many2one('product.product')
    qty = fields.Float('Quantity')
    price = fields.Float('Price')
    quote_id = fields.Many2one('quote.order', 'Quote Order')
    
    def unlink(self):
        return super(QuoteOrderLine, self).unlink()
    
    
class QuoteOrder(models.Model):
    
    _name = 'quote.order'
    _description = "Quote Order"
    
    partner_id = fields.Many2one('res.partner')
    quote_lines = fields.One2many('quote.order.line', 'quote_id', 'Quote Lines')


    def unlink(self):
        for qt in self:
            qt.sudo().quote_lines.unlink()
        return super(QuoteOrder, self).unlink()


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'


    last_website_quote_id = fields.Many2one('quote.order', compute='_compute_last_website_quote_id', string='Last Online Quote Order')
    project = fields.Char(string='Project')

    def _compute_last_website_quote_id(self):
        QuoteOrder = self.env['quote.order']
        for partner in self:
            is_public = any([u._is_public()
                             for u in partner.with_context(active_test=False).user_ids])
            website = ir_http.get_request_website()
            if website and not is_public:
                partner.last_website_quote_id = QuoteOrder.search([
                    ('partner_id', '=', partner.id),
                ],order='id desc',  limit=1)
            else:
                partner.last_website_quote_id = QuoteOrder

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_web_quotation = fields.Boolean(string='Is Website Quotation',store=True,copy=True)
    project = fields.Char('Project Name')
   
    state = fields.Selection(selection_add=[('rfq', 'RFQ'), ('draft',)])
    
    def confirm_rfq(self):        
        return self.write({'state': 'draft'})