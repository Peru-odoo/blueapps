# -*- coding: utf-8 -*-
from odoo import http


class ResetCampaign(http.Controller):
    @http.route('/asterisk_dialer/reset_campaign', auth='user', csrf=False)
    def index(self, **kw):
        campaign_name = kw.get('campaign_name')
        if campaign_name is None:
            return "Please add a campaign name"
        campaign = http.request.env['asterisk_dialer.campaign'].search(
            [('name', '=', campaign_name)], limit=1)
        if not campaign:
            return 'No campaign found'
        campaign.contacts.write({'state': 'q'})
        campaign.wakeup()
        return "Campaign {} reset successfully".format(campaign_name)

