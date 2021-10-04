# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import models, fields, api, tools, release, _
from odoo.exceptions import ValidationError, UserError

logger = logging.getLogger(__name__)


class ResUser(models.Model):
    _inherit = 'res.users'

    dialer_operator = fields.One2many(
        'asterisk_dialer.operator', inverse_name='user')
    dialer_operator_accountcode = fields.Char(
        related='dialer_operator.accountcode')


