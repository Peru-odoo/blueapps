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
from datetime import date

class LeadSummaryWizard(models.TransientModel):
    _name = "lead.summary.wizard"
    _description = "Lead Summary Wizard"

    user_id = fields.Many2one("res.users", string="Salesperson")
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")

    #Using object button of print in wizard for get report pdf
    def print_report(self):
        data = {
            'doc_model': 'lead.summary.wizard',
            'user_id' : self.user_id.id,
            'start_date' : self.start_date,
            'end_date' : self.end_date,
        }
        return self.env.ref('blue_comissao_consultores_aguias.action_report_lead_summary').report_action(self, data=data)
        




    



        
