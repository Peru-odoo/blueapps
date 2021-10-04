import logging
from odoo import models, fields
from odoo.tools import mute_logger
from psycopg2 import IntegrityError

logger = logging.getLogger(__name__)


class AddContactWizard(models.TransientModel):

    _name = 'asterisk_dialer.add_contact_wizard'
    _description = 'Add contact to campaign'

    campaign = fields.Many2one('asterisk_dialer.campaign')

    def add_contact(self):
        domain = [('id', 'in', self._context.get('active_ids', []))]
        self.campaign.generate_contacts('res.partner', domain)
