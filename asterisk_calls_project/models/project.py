import logging
from phonenumbers import phonenumberutil
import phonenumbers
from odoo import api, models, tools, fields, release, _
from odoo.exceptions import ValidationError, UserError

logger = logging.getLogger(__name__)


class Project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    asterisk_calls_count = fields.Integer(compute='_get_asterisk_calls_count',
                                          string=_('Calls'))
    partner_phone = fields.Char(related='partner_id.phone')
    partner_mobile = fields.Char(related='partner_id.mobile')
    recorded_calls = fields.One2many(
        'asterisk_calls.call', 'project',
        domain=[('recording_filename', '!=', False)])

    def _get_asterisk_calls_count(self):
        for rec in self:
            rec.asterisk_calls_count = self.env[
                'asterisk_calls.call'].search_count([('project', '=', rec.id)])

    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)
        try:
            if self.env.context.get('create_call_project'):
                call = self.env['asterisk_calls.call'].browse(
                    self.env.context['create_call_project'])
                call.project = res.id
        except Exception as e:
            logger.exception(e)
        return res
