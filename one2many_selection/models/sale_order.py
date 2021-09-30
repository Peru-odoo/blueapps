
from odoo import models, fields, api

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	# Demo method that will delete your sale orde line as you select and press delete
	@api.model
	def delete_sale_order_lines(self, selected_ids):
		orderline_sudo = self.env['sale.order.line'].sudo()
		order_lines = orderline_sudo.browse(selected_ids)
		for line in order_lines:
			line.unlink()
		return True