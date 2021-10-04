# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import models, fields, api

logger = logging.getLogger(__name__)


class ResUser(models.Model):
    _inherit = 'res.users'

    calls_open_partner_form = fields.Boolean(
        related='asterisk_user.open_partner_form')

    @api.model
    def get_asterisk_channels(self, uid):
        # Used from channels.js
        res = {}
        user_channels = self.env['asterisk_common.user_channel'].search(
            [('user', '=', uid)])
        for user_channel in user_channels:
            res.setdefault(
                user_channel.system_name, []).append(user_channel.channel)
        return res
