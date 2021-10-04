# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import fields, models, api, addons, _
from odoo.tools import ormcache


logger = logging.getLogger(__name__)


class DialerSettings(models.Model):
    _inherit = 'asterisk_common.settings'

    default_provider = fields.Char(
        help=_("Default 'Channel Provider' setting for new campaigns.")
    )
    dial_attempts = fields.Integer(
        default=2,
        help=_("Default 'Dial Attempts' setting for new campaigns.")
    )
    default_campaign = fields.Many2one('asterisk_dialer.campaign',
        help=_("Default 'Campaign' for new contacts.")
    )
