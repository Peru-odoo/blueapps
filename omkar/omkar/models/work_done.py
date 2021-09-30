from odoo import api, fields, models, _


class WorkDone(models.Model):
	_name = "work.done"
	_description = "bill"

	sr_no = fields.Char(readonly=True, copy=False, index=True, default=lambda self: _('New'))
	product_name = fields.Char("Product Name", required=True)
	description = fields.Char('Description')
	sequence = fields.Integer()
	quantity = fields.Float("Quantity", required=True, digits=(2,2))
	currency_id = fields.Many2one('res.currency', string="Currency", readonly=True,
                                  default=lambda self: self.env['res.currency'].browse([20]),
                                  invisible=True)   
	unit_price = fields.Float("Unit Price", required=True, digits=(5,2))
	subtotal = fields.Monetary("Sub Total", compute="calculate_subtotal", store=True)
	customer_id = fields.Many2one('omkar.customer')


	@api.depends('quantity', 'unit_price')
	def calculate_subtotal(self):
		for rec in self:
			rec.subtotal = rec.quantity * rec.unit_price

	@api.onchange('product_name')
	def get_desc(self):
		for rec in self:
			rec.description = rec.product_name
			
	