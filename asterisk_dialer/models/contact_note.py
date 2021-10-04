# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import models, fields, api, _
try:
    import humanize
    HUMANIZE = True
except ImportError:
    HUMANIZE = False

logger = logging.getLogger(__name__)


class ContactNote(models.Model):
    _name = 'asterisk_dialer.contact_note'
    _description = _('Dialer Contact Note')
    _order = 'id desc'

    note = fields.Text()
    contact = fields.Many2one('asterisk_dialer.contact')
    create_date_human = fields.Char(compute='_get_humanized_create_date', string='Created')

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
