# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)


class AsteriskUserChannel(models.Model):
    _inherit = 'asterisk_common.user_channel'

    is_queue = fields.Boolean(string="Queue")


class AsteriskUser(models.Model):
    _inherit = 'asterisk_common.user'

    queue_interface = fields.Char()

    @api.constrains('channels')
    def _set_queue_interface(self):
        is_queue_count = 0
        for channel in self.channels:
            if channel.is_queue:
                self.queue_interface = channel.comp_channel
                is_queue_count += 1
                if is_queue_count > 1:
                    raise ValidationError(_('Only one channel can be configured as queue!'))
        if is_queue_count == 0:
            logger.warning('Queue count is 0')

    def write(self, vals):
        res = super(AsteriskUser, self).write(vals)
        if not self.env.context.get('no_build_conf'):
            self.build_conf()
            self.env['asterisk_base_queues.queue'].build_conf()
        return res
