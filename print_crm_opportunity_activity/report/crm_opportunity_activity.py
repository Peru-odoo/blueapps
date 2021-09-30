# -*- coding: utf-8 -*-

import time
from odoo import api, models

class CRMOpportunityActivity(models.AbstractModel):
    _name = "report.print_crm_opportunity_activity.opportunity_activity_id"
    
    def get_opportunity_meeting(self, opportunity):
        calender_obj = self.env['calendar.event'].search([('opportunity_id', 'in', opportunity)])
        return calender_obj
    
    @api.model
    #def render_html(self, docids, data=None):
    def _get_report_values(self, docids, data=None):                    # odoo 11
        report = self.env['ir.actions.report']._get_report_from_name('print_crm_opportunity_activity.opportunity_activity_id')
        get_meetings = self.get_opportunity_meeting(docids)
        opportunity = self.env['crm.lead'].browse(docids)
        #docargs = {
        return {
            'doc_ids': docids,
            'doc_model': 'crm.lead',
            'data': data,
            'docs': self.env['crm.lead'].browse(docids),
            'get_meetings': get_meetings
        }
        #return self.env['report'].render('print_crm_opportunity_activity.opportunity_activity_id', docargs)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
