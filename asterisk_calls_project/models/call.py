import json
import logging
from odoo import models, fields, api, _

logger = logging.getLogger(__name__)


class ProjectCall(models.Model):
    _name = 'asterisk_calls.call'
    _inherit = 'asterisk_calls.call'

    task = fields.Many2one('project.task')
    project = fields.Many2one('project.project')

    @api.model
    def create(self, vals):
        # Find a task with a call id from channel
        task = self.env['project.task'].search(
            [('last_call_id', '=', vals.get('uniqueid'))])
        if task:
            vals['task'] = task.id
            vals['project'] = task.project_id.id
        return super(ProjectCall, self).create(vals)

    @api.model
    def update_cdr_values(self, original_vals):
        vals = super(ProjectCall, self).update_cdr_values(original_vals)
        # Check if it is orginated call
        originate_data = self.env['kv_cache.cache'].get(
            original_vals.get('uniqueid'), tag='originated_call',
            serialize='json')
        if not originate_data:
            originate_data = self.env['kv_cache.cache'].get(
                original_vals.get('linkedid'), tag='originated_call',
                serialize='json')
            if originate_data:
                logger.debug('FOUND PROJECT ORIGINATED CALL DATA FROM LINKEDID.')
        model = originate_data.get('model')
        res_id = originate_data.get('res_id')
        project = task = None
        # Try to get project or task from originated call data.
        if model == 'project.project' and res_id:
            logger.debug('FOUND PROJECT FROM ORIGINATED CALL DATA.')
            vals.update({'project': res_id})
            project = self.env['project.project'].browse(res_id)
            vals['project'] = project.id
        elif model == 'project.task' and res_id:
            logger.debug('FOUND TASK FROM ORIGINATED CALL DATA.')
            vals.update({'task': res_id})
            task = self.env['project.task'].browse(res_id)
            vals['task'] = task.id
            vals['project'] = task.project_id.id
        elif vals.get('partner'):
            logger.debug('PROJECT OR TASK NOT FOUND BY ORIGINATED CALL DATA')
            # Get types with sudo in order to not define a security rule.
            open_task_statuses_ids = [k.id for k in self.env[
                'project.task.type'].sudo().search([('is_closed', '=', False)])]
            task = self.env['project.task'].search(
                [('partner_id', '=', vals['partner']),
                 ('stage_id', 'in', open_task_statuses_ids)],
                limit=1, order='id desc')
            if task:
                logger.debug('CHANNEL TASK FOUND BY PARTNER')
                vals['task'] = task.id
                vals['project'] = task.project_id.id
            else:
                # Task not found, search project
                project = self.env['project.project'].search(
                    [('partner_id', '=', vals['partner'])],
                    limit=1, order='id desc')
                if project:
                    logger.debug('CHANNEL PROJECT FOUND BY PARTNER')
                    vals['project'] = project.id
        return vals

    def create_task(self):
        self.ensure_one()
        return {
            'res_model': 'project.task',
            'name': _('Create  Task'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_phone': self.dst if self.src_user else self.src,
                'default_name': self.partner.name if self.partner else self.clid,
                'default_partner_id': self.partner.id if self.partner else False,
                'default_project_id': self.project.id,
                'create_call_task': self.id,
            },
        }

    def create_project(self):
        self.ensure_one()
        return {
            'res_model': 'project.project',
            'name': _('Create Project'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_phone': self.dst if self.src_user else self.src,
                'default_name': self.partner.name if self.partner else self.clid,
                'default_partner_id': self.partner.id if self.partner else False,
                'default_project_id': self.project.id,
                'create_call_project': self.id,
            },
        }
