# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import datetime
from odoo import http
from odoo.http import request
import json
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

	@http.route()
	def products_autocomplete(self, term, options={}, **kwargs):

		res = super(WebsiteSale, self).products_autocomplete(
			term, options=options, **kwargs)
		products_ids = [product['id'] for product in res['products']]
		products = request.env['product.template'].browse(products_ids)
		for res_product, product in zip(res['products'], products):
			res_product['quote_products'] = not product.quote_products
			res_product['list_price'] = not product.list_price
			res_product['is_extra_price'] = not product.is_extra_price
			print ("res_product['is_extra_price']",res_product['is_extra_price'])
		return res

	def _get_products_recently_viewed(self):
		res = super(WebsiteSale, self)._get_products_recently_viewed()		
		if res:			
			products_ids = [product['id'] for product in res['products']]
			products = request.env['product.product'].browse(products_ids)
			for res_product, product in zip(res['products'], products):
				res_product['quote_products'] = not product.quote_products
		return res

class OdooWebsiteProductQuote(http.Controller):

	# @http.route(['/shop'], type='http', auth="public", website=True)
	# def quote(self, **post):
	# 	cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
	# 	return request.render("website_rfq.quote")

	@http.route(['/shop/quote/add'], type='json', auth="public", website=True)
	def add_to_quote(self, product_id, **kw):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		product_id = int(product_id)		
		quote_obj = request.env['quote.order']
		quote_line_obj = request.env['quote.order.line']
		partner = request.env.user.partner_id		
		quote_order_id = request.session.get('quote_order_id')
		if not quote_order_id:
			last_quote_order = partner.last_website_quote_id
			quote_order_id = last_quote_order.id

		quote_order = request.env['quote.order'].sudo().browse(quote_order_id).exists() if quote_order_id else None		
		product_product_obj = request.env['product.product'].sudo().search([('id','=', product_id)], limit=1)		
		request.session['quote_order_id'] = None
		if not quote_order:
			quote = quote_obj.sudo().create({'partner_id': partner.id})
			quote_line_ids = quote_line_obj.sudo().search([('product_id.id','=', product_id),('quote_id','=',quote.id)])
			
			if quote_line_ids:
				quote_line_ids.update({'qty': quote_line_ids.qty})
			else:
				quote_line = quote_line_obj.sudo().create({
					'product_id': product_product_obj.id,
					'qty': 1,
					'price': product_product_obj.lst_price,
					'quote_id': quote.id,	
				})
			request.session['quote_order_id'] = quote.id
		if quote_order:			
			if not request.session.get('quote_order_id'):
				request.session['quote_order_id'] = quote_order.id
			
			quote_line_ids = quote_line_obj.sudo().search([('product_id.id','=', product_id),('quote_id','=',quote_order.id)])
			if quote_line_ids:
				quote_line_ids.update({'qty': quote_line_ids.qty})
			else:				
				quote_line = quote_line_obj.sudo().create({
					'product_id': product_product_obj.id,
					'qty': 1,
					'price': product_product_obj.lst_price,
					'quote_id': quote_order.id,	
				})		 

	@http.route('/shop/_get_product_id', type='json', auth='public', website=True)
	def _get_product_id(self, product_tmpl_id):
		product_ids = request.env['product.product'].search([('id','=',product_tmpl_id)],limit=1)
		print ("------>>mm",product_ids)       
		return product_ids

	@http.route(['/shop/quote'], type='http', auth="public", website=True)
	def quote_cart(self, access_token=None, revive='', **post):		
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		
		return request.render("website_rfq.quote_cart")

	@http.route(['/shop/product/selected/nonlogin'], type='http', auth="public", website=True)
	def quote_multiple_nonlogin(self, **post):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		countries = request.env['res.country'].sudo().search([])
		states = request.env['res.country.state'].sudo().search([])
		values ={}
		values.update({
					'countries': countries,
					'states': states,
			})		
		return request.render("website_rfq.get_quotation_request",values)

	@http.route(['/shop/quote/update_json'], type='json', auth="public", website=True)
	def get_cart_qty(self,jsdata, **post):	
		
		quote_cart_ids =request.env['quote.order'].sudo().browse(request.session['quote_order_id'])

		for i in quote_cart_ids.quote_lines:
			for j in jsdata:
				for x, y in j.items():
					
					if i.id == int(x):
						
						i.update({'qty': y})
		return True	
		
	@http.route(['/process/quote'], type='http', auth="public", website=True)
	def get_quote(self, **post):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		order =request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
		# print ("----------------order quote id>>>",order)
		val={'order':order}
		return request.render("website_rfq.get_billing",val)

		# if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
  #           return request.redirect('/shop/address')

		# for f in self._get_mandatory_billing_fields():
  #           if not order.partner_id[f]:
  #               return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)

  #   def _get_mandatory_billing_fields(self):
  #       return ["name", "email", "street", "city", "country_id"]

	@http.route(['/process/quote/nonlogin'], type='http', auth="public", website=True)
	def get_quote_nonlogin(self, **post):
		if not post.get('debug'):
			cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
			# print("-------------------------------------------------NON LOGIN PAGE------------",request.session.uid,post['phone'])
			if post['state_id']:
				state_id = int(post['state_id'])
			else:
				state_id = False

			if post['company']:

				partner_obj = request.env['res.partner']
				partner = partner_obj.sudo().create({ 
				  'name' : post['company'],
				  # 'email' : post['email'],
				  # 'phone' : post['phone'],
				  'street': post['street'],
				  'city':post['city'],
				  'zip':post['zip'],
				  'country_id':int(post['country_id']) if post['country_id'] else False,
				  'state_id': state_id,
				  'company_type':'company',
				  # 'project':post['projectname'],

				})
				if partner:					
					user_obj = request.env['res.users'].sudo().browse(request.session.uid)
					# partner_obj = request.env['res.partner'].sudo().browse(user_obj.sudo().partner_id.id)			
					partner_obj = request.env['res.partner'].sudo().search([('id','=',user_obj.sudo().partner_id.id)])
					print("partner id>>" ,partner_obj)
					partner_obj.update({'phone':post['phone'],
						'name' : post['name'],
						'street': post['street'],
						'city':post['city'],
						'zip':post['zip'],
						'country_id':int(post['country_id']) if post['country_id'] else False,
						'state_id': state_id,
						'parent_id':partner.id,
						'project':post['projectname'],
						})
			else:
				user_obj = request.env['res.users'].sudo().browse(request.session.uid)
				# partner_obj = request.env['res.partner'].sudo().browse(user_obj.sudo().partner_id.id)			
				partner_obj = request.env['res.partner'].sudo().search([('id','=',user_obj.sudo().partner_id.id)])
				print("partner id>>" ,partner_obj)
				partner_obj.update({'phone':post['phone'],
				'name' : post['name'],
				'street': post['street'],
				'city':post['city'],
				'zip':post['zip'],
				'country_id':int(post['country_id']) if post['country_id'] else False,
				'state_id': state_id,
				'project':post['projectname'],				
				})
			

			order = request.env['quote.order'].sudo().search([],order='id desc', limit=1)
			order.update({'partner_id':user_obj.sudo().partner_id.id})
			# order = request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
			# order.update({'partner_id':partner_obj.id})
			# product_obj = request.env['product.template']        
			# sale_order_obj = request.env['sale.order']
			# sale_order_line_obj = request.env['sale.order.line']
			# line_vals ={}
			# pricelist_id = request.website.get_current_pricelist().id
			# vals = {
			# 		'partner_id': partner_obj.id, 
			# 		'pricelist_id': pricelist_id,
			# 		'user_id': request.website.salesperson_id and request.website.salesperson_id.id,
			# 		'team_id': request.website.salesteam_id and request.website.salesteam_id.id
			# 	}    	
			# sale_order_create = sale_order_obj.sudo().create(vals)
			# for i in order.quote_lines:
			# 	line_vals = {    
			# 				'product_id': i.product_id.id, 
			# 				'name': i.product_id.name,
			# 				'product_uom_qty': i.qty, 
			# 				'customer_lead':7, 
			# 				'product_uom':i.product_id.uom_id.id,
			# 				'order_id': sale_order_create.id  }
			# 	sale_order_line_create = sale_order_line_obj.sudo().create(line_vals)
			
			# order.sudo().unlink()
			# request.session['quote_order_id'] = False
			return request.render("website_rfq.quote_thankyou")

	@http.route(['/shop/product/quote/confirm'], type='http', auth="public", website=True)
	def quote_confirm(self, **post):
		if not post.get('debug'):			
			return request.render("website_rfq.quote_thankyou")

	@http.route(['/shop/product/quote/confirmclone'], type='http', auth="public", website=True)
	def quote_confirmclone(self, **post):
		if not post.get('debug'):
			order = request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
			if not order:
				order = request.env['quote.order'].sudo().search([],order='id desc', limit=1)
			project_ids = request.env['res.partner'].sudo().search([('id','=',order.partner_id.id)])			
			product_obj = request.env['product.template']        
			partner_obj = request.env['res.partner']
			sale_order_obj = request.env['sale.order']
			sale_order_line_obj = request.env['sale.order.line']
			line_vals ={}
			pricelist_id = request.website.get_current_pricelist().id
			print ("partner_id",order.partner_id.id)
			vals = {
					'partner_id': order.partner_id.id,
					'project': project_ids.project,
					'is_web_quotation':True,
					'pricelist_id': pricelist_id,
					'user_id': request.website.salesperson_id and request.website.salesperson_id.id,
					'team_id': request.website.salesteam_id and request.website.salesteam_id.id,
					'website_id':request.website.id,
					'state':'rfq',
				} 
			sale_order_create = sale_order_obj.sudo().create(vals)
			for i in order.quote_lines:
				line_vals = {    
							'product_id': i.product_id.id, 
							'name': i.product_id.name,
							'product_uom_qty': i.qty, 
							'customer_lead':7, 
							'product_uom':i.product_id.uom_id.id,
							'order_id': sale_order_create.id  }
				
				sale_order_line_create = sale_order_line_obj.sudo().create(line_vals)			
			order.sudo().unlink()
			request.session['quote_order_id'] = False
			return request.render("website_rfq.quote_final_page")

	@http.route(['/quote/delete/<model("quote.order.line"):line>'], type='http', auth="public", website=True)
	def qoute_delete(self, **post):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		order = post['line']
		
		order.sudo().unlink()
		return request.render("website_rfq.quote_cart")	

	@http.route(['/thank_you'], type='http', auth="public", website=True)
	def thank_you(self, **post):
		if not post.get('debug'):
			cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
			return request.render("website_rfq.quote_thankyou")

	@http.route(['/shop/quote/print'], type='http', auth="public", website=True, sitemap=False)
	def print_quotation(self, **kwargs):		
		sale_order_id = request.env['sale.order'].sudo().search([],order='id desc', limit=1)		
		if sale_order_id:
			pdf, _ = request.env.ref('website_rfq.action_report_saleorder_rfq').sudo()._render_qweb_pdf([sale_order_id.id])
			pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', u'%s' % len(pdf))]
			return request.make_response(pdf, headers=pdfhttpheaders)
		else:
			return request.redirect('/shop')
				
