# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import models, fields, api, tools, registry, release, _
from odoo.exceptions import ValidationError, UserError

logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    asterisk_server = fields.One2many('asterisk_base.server',
                                      inverse_name='user')

