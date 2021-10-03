# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Botspot Infoware Pvt ltd'<www.botspotinfoware.com>
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
from odoo import api, fields, models, _


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    total_sales_by_employee = fields.Float(string="Total sales by employee", compute="compute_total")
    opportunity_count = fields.Integer(string="Opportunities", compute="compute_count")
    total_commission = fields.Float(string="Total Commission", compute="compute_commission")
    commission_rule_id = fields.Many2one("crm.commission.rule", string="Commission Rule")

    # This Compute method used for leads count in opportunities we can see employee's all leads in opportunities...
    def compute_count(self):
        for record in self:
            record.opportunity_count = self.env['crm.lead'].search_count([('user_id', '=', record.user_id.id)])

    # Used for employee's leads
    def get_leads(self):
        self.ensure_one()
        return{
            'name': 'Leads',
            'res_model': 'crm.lead',
            'domain': [('user_id', '=', self.user_id.id)],
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'context': "{'create': False}"
        }

    #For using compute method total leads's expected revenue sum in employee total leads by employee... 
    def compute_total(self):
        for record in self:
            lead_amout = 0.0
            lead_ids = self.env['crm.lead'].search([('user_id', '=', record.user_id.id)])
            if lead_ids:
                lead_amout = 0.0
                for lead in lead_ids:
                    lead_amout += lead.expected_revenue
            record.total_sales_by_employee = lead_amout

    #For calculate total commision
    def compute_commission(self):
        for record in self:
            if record.commission_rule_id.commission_type == 'percentage':
                percentage_count = record.total_sales_by_employee*record.commission_rule_id.commission/100
                record.total_commission = percentage_count
            else:
                record.commission_rule_id.commission_type == 'amount'
                amount_count = record.commission_rule_id.commission
                record.total_commission = amount_count
