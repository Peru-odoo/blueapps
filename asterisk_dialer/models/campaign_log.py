# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import models, fields, api, _
try:
    import humanize
    HUMANIZE = True
except ImportError:
    HUMANIZE = False

logger = logging.getLogger(__name__)

LOG_LEVELS = [
    ('i', 'Info'),
    ('d', 'Debug'),
]


class CampaignLog(models.Model):
    _name = 'asterisk_dialer.campaign_log'
    _description = _('Dialer Campaign Log')
    _order = 'id desc'
    _rec_name = 'id'

    campaign = fields.Many2one('asterisk_dialer.campaign', ondelete='cascade')
    level = fields.Selection(
        LOG_LEVELS,
        index=True, readonly=True, default='i', required=True)
    content = fields.Text()
    create_date_human = fields.Char(
        compute='_get_humanized_create_date', string='Created')
    active = fields.Boolean(default=True, index=True)

    @api.depends('create_date')
    def _get_humanized_create_date(self):
        global HUMANIZE
        if HUMANIZE:
            try:
                to_translate = self.env.context.get('lang', 'en_US')
                if to_translate != 'en_US':
                    humanize.i18n.activate(to_translate)
            except Exception:
                HUMANIZE = False
        for rec in self:
            if HUMANIZE:
                rec.create_date_human = humanize.naturaltime(fields.Datetime.from_string(rec.create_date))
            else:
                rec.create_date_human = str(rec.create_date)
