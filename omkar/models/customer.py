# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date

class Customer(models.Model):
    _name = 'omkar.customer'
    _description = 'omkar.omkar'

    name = fields.Char(required=True)
    bill_no = fields.Char(string='Bill No', readonly=True, required=True, store=True, copy=False, index=True, default=lambda self: _('New'))
    vehicle_model = fields.Char(required=True)
    vehicle_no = fields.Char(required=True, default="GJ10XX2512")
    address = fields.Text('Address')
    mobile_no = fields.Char('Mobile No.')
    kilometers = fields.Float('Vehicle kilometers', digits=(6,2))
    issue_date = fields.Date('Issue Date', default=date.today())
    work_done_date = fields.Date('Billing Date')
    customer_of = fields.Selection([('bansi', 'Bansi Ka.patel'), ('kishan', 'Kishan Gajera')], default='bansi')
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True,
                                  default=lambda self: self.env['res.currency'].browse([20]),
                                  invisible=True)    
    work_lines = fields.One2many('work.done', 'customer_id', "Work done", default=[(0,0,{'product_name': 'Service Charge', 'quantity': 1.00,'unit_price' : 1000})])
    total = fields.Monetary(string="Total Amount", default = 0, compute="calculate_total", store=True)
    paid = fields.Boolean(string="Paid or Not")
    state = fields.Selection([('paid', 'Paid'), ('notpaid','Payment Due')], default="notpaid")
    signature = fields.Binary("Signature")


    @api.onchange('vehicle_no')
    def set_upper(self):
        self.vehicle_no = str(self.vehicle_no).upper()

    @api.depends('work_lines.subtotal')
    def calculate_total(self):
        """
        Compute the total amounts of the work.
        """
        for order in self:
            total = 0.0
            for line in order.work_lines:
                total += line.subtotal
            order.update({
                'total': total,
            })


    def name_get(self):
        res = []
        for rec in self:
            name = f"{rec.name}[{rec.vehicle_model}]"
            res.append((rec.id, name))
        return res

    @api.onchange('paid')
    def state_assign(self):
        for rec in self:
            if rec.paid == True:
                rec.state = 'paid'
            else:
                rec.state == 'notpaid'

    @api.model
    def create(self, vals):
        if vals.get('bill_no', 'New') == 'New':
            vals['bill_no'] = self.env['ir.sequence'].next_by_code(
                'omkar.customer') or 'New'

        result = super(Customer, self).create(vals)
        return result


    # def default_get(self, fields):
    #     res = super(Customer, self).default_get(fields)
    #     srd = self.env['omkar.customer']
    #     ids=[]
    #     result={'product_name': 'Service Charge','unit_price':1000} #dict for fields and their values
    #     sr = srd.create(result)
    #     ids.append(sr.id)


    #     res['work_lines'] = ids
    #     return res