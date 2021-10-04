import logging
from phonenumbers import phonenumberutil
import phonenumbers
from odoo import api, models, tools, fields, release, _
from odoo.exceptions import ValidationError, UserError

logger = logging.getLogger(__name__)


class Task(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    asterisk_calls_count = fields.Integer(compute='_get_asterisk_calls_count',
                                          string=_('Calls'))
    partner_phone = fields.Char(related='partner_id.phone')
    partner_mobile = fields.Char(related='partner_id.mobile')
    recorded_calls = fields.One2many(
        'asterisk_calls.call', 'task',
        domain=[('recording_filename', '!=', False)])
    # Keep here call id from which task was created.
    last_call_id = fields.Char()

    def _get_asterisk_calls_count(self):
        for rec in self:
            rec.asterisk_calls_count = self.env[
                'asterisk_calls.call'].search_count([('task', '=', rec.id)])

    @api.model
    def create(self, vals):
        # Check if it is a create task from active call operation.
        if self.env.context.get('channel_uniqueid'):
            vals['last_call_id'] = self.env.context.get('channel_uniqueid')
        res = super(Task, self).create(vals)
        # Now bind task to the channel
        if self.env.context.get('channel_uniqueid'):
            channel = self.env['asterisk_calls.channel'].search(
                [('uniqueid', '=', self.env.context.get('channel_uniqueid'))])
            channel.write({'task': res.id, 'project': res.project_id.id})
        try:
            if self.env.context.get('create_call_task'):
                call = self.env['asterisk_calls.call'].browse(
                    self.env.context['create_call_task'])
                call.write({
                    'task': res.id,
                    'project': res.project_id.id,
                })
        except Exception as e:
            logger.exception(e)
        return res
