import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Customer(models.Model):
    _inherit = 'sale.order'

    kw_phone = fields.Char(
        related='partner_id.phone',
        string='Phone')
