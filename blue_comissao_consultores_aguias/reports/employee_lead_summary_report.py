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

from odoo import api, models, _
from datetime import date
from odoo.exceptions import UserError

class LeadSummaryReport(models.AbstractModel):
    _name = 'report.blue_comissao_consultores_aguias.lead_summary'
    _description = 'Lead Summary Report'

    #Getting all records from wizard and print record in report and also raise usererror when no leads are available for this sales person. and return all the records in report pdf..
    @api.model
    def _get_report_values(self, docids, data=None):
        lead_ids = False
        user_id = False
        if data['user_id']:
            user_id = self.env['res.users'].browse(data['user_id'])
            employee_id = self.env['hr.employee'].search([('user_id', '=', int(data['user_id']))])
            lead_ids = self.env['crm.lead'].search([('user_id', '=', int(data['user_id'])),
                                                    ('date_open', '>=', (data['start_date'])),
                                                    ('date_open', '<=', (data['end_date']))])
            if not lead_ids:
                raise UserError(_("in this time frame no leads available for this sales person"))        
        return {
            'user_id': user_id,
            'total_sales_by_employee' : employee_id.total_sales_by_employee,
            'commission_rule_id' : employee_id.commission_rule_id,
            'total_commission' : employee_id.total_commission,
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'lead_ids': lead_ids
        }
        






      
