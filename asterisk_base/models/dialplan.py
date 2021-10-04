# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
from jinja2.sandbox import SandboxedEnvironment
import logging
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import ustr
from ..utils import is_debug_mode_enabled
from ..utils import get_default_server


logger = logging.getLogger(__name__)

DIALPLAN_TYPES = [
    ('standard', 'Standard'),
    ('service', 'Service')
]


# TODO: Remove this model after updates.
class DialplanVariable(models.Model):
    _name = 'asterisk_base.dialplan_variable'
    _description = 'Dialplan Variables'

    name = fields.Char(required=True)
    value = fields.Char()
    is_dynamic = fields.Boolean(string='Dynamic?')


class Dialplan(models.Model):
    _name = 'asterisk_base.dialplan'
    _description = "Dialplan"

    dialplan_type = fields.Selection(DIALPLAN_TYPES, required=True,
                                     default='standard', string='Type')
    server = fields.Many2one(
        comodel_name='asterisk_base.server', required=True,
        default=get_default_server)
    name = fields.Char()  # TODO: required=True)
    extension = fields.Many2one('asterisk_base.extension')
    exten = fields.Char(related='extension.number', readonly=False)
    note = fields.Text()
    lines = fields.One2many(
        'asterisk_base.dialplan_line', inverse_name='dialplan')
    is_custom = fields.Boolean(string="Custom")
    is_protected = fields.Boolean(string='Read Only')
    custom_dialplan = fields.Text(string='Dialplan')
    dialplan = fields.Text(compute='_get_dialplan')
    context = fields.Text(compute='_get_context')
    # TODO: Remove after updates.
    variables = fields.Many2many('asterisk_base.dialplan_variable')

    _sql_constraints = []

    @api.model
    def create(self, vals):
        res = super(Dialplan, self).create(vals)
        if res and not self.env.context.get('no_build_conf'):
            if res.exten:
                self.env['asterisk_base.extension'].create_extension_for_obj(
                    res, exten_type=res.dialplan_type)
            self.build_conf()
        return res

    def write(self, vals):
        if 'exten' in vals:
            for rec in self:
                rec.extension and rec.extension.unlink()
        res = super(Dialplan, self).write(vals)
        if ('install_mode' not in self.env.context and
                not is_debug_mode_enabled()):
            for rec in self:
                if rec.is_protected:
                    raise ValidationError(
                        _('Activate developer mode to change '
                          'a protected dialplan!'))
        if 'exten' in vals:
            for rec in self:
                if rec.exten:
                    model = self.env['asterisk_base.extension']
                    model.create_extension_for_obj(rec)
        if res and not self.env.context.get('no_build_conf'):
            self.build_conf()
            self.env['asterisk_base.extension'].build_conf()
        return res

    def unlink(self):
        for rec in self:
            # Check if it is a read only dialplan
            if rec.is_protected:
                if 'install_mode' in self.env.context:
                    pass
                elif '_force_unlink' in self.env.context:
                    pass
                elif is_debug_mode_enabled():
                    pass
                else:
                    raise ValidationError(
                        _('Activate developer mode to delete a protected dialplan!'))
            if rec.extension:
                rec.extension.unlink()
        res = super(Dialplan, self).unlink()
        if res:
            self.build_conf()
            self.env['asterisk_base.extension'].build_conf()
        return res

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({
            'exten': '{}-1'.format(self.exten),
            'name': '{}-copy'.format(self.name),
            'extension': False,
        })
        if not self.is_custom:
            # Copy lines
            new_lines = []
            for line in self.lines:
                new_line = self.env['asterisk_base.dialplan_line'].create({
                    'exten': line.exten,
                    'sequence': line.sequence,
                    'app': line.app,
                    'app_data': line.app_data,
                    'label': line.label
                })
                new_lines.append([4, new_line.id, 0])
            default['lines'] = new_lines
        else:
            default['custom_dialplan'] = self.custom_dialplan
        return super(Dialplan, self).copy(default)

    def build_extension(self):
        # Render extension from template
        self.ensure_one()
        return self.env[
            'asterisk_base.conf_template'].render_template(
            'extension_dialplan', self.server.id, {'rec': self})

    def build_dialplan(self, force_from_wizard=False):
        self.ensure_one()
        # Custom DP
        if not force_from_wizard and self.is_custom:
            if self.dialplan_type != 'service':
                # Add [dialplan-id] for service dialplans
                return '; {}\n[dialplan-{}]\n{}\n'.format(
                    self.name, self.id, self.custom_dialplan)
            else:
                # Do not add [dialplan-id] for service dialplans
                return '; {}\n{}\n'.format(self.name, self.custom_dialplan)
        # Wizard
        else:
            ret_lines = [
                '; {}'.format(self.name),
                '[dialplan-{}]'.format(self.id),
                'exten => {},1,NoOp(Dialplan {})'.format(self.exten, self.name)
            ]
            for line in self.lines:
                if not line.label:
                    ret_lines.append('same => n,{}({})'.format(
                        line.app, line.app_data if line.app_data else ''))
                else:
                    ret_lines.append('same => n({}),{}({})'.format(
                        line.label, line.app,
                        line.app_data if line.app_data else ''))
            ret_lines.append('\n')
            return '\n'.join(ret_lines)

    @api.model
    def render_dialplan(self, template_txt, rec):
        template_env = SandboxedEnvironment(
            lstrip_blocks=True,
            trim_blocks=False,
            keep_trailing_newline=True,
            autoescape=False,
        )
        template = template_env.from_string(ustr(template_txt))
        variables = {'rec': rec}
        return template.render(variables)

    @api.model
    def build_conf(self):
        dialplans = self.env['asterisk_base.dialplan'].search([], order='id')
        for server in dialplans.mapped('server'):
            conf_data = ''
            for dp in dialplans.filtered(lambda r: r.server == server):
                conf_data += dp.build_dialplan() or ''
                conf_data = self.render_dialplan(conf_data, dp)
            conf = self.env['asterisk_base.conf'].get_or_create(
                server.id, 'extensions_odoo_dialplan.conf')
            conf.content = '{}'.format(conf_data)
            conf.include_from('extensions.conf')

    def _get_context(self):
        for rec in self:
            rec.context = 'dialplan-{}'.format(rec.id)

    @api.depends('lines')
    def _get_dialplan(self):
        for rec in self:
            rec.dialplan = rec.build_dialplan()

    def _set_dialplan(self):
        for rec in self:
            rec.custom_dialplan = rec.dialplan

    @api.onchange('is_custom')
    def _build_dialplan_from_wizard(self):
        if self.is_custom:
            # Copy from wizard only the first time!
            if self._origin and not self.custom_dialplan:
                dp = self._origin.build_dialplan(force_from_wizard=True)
                self.custom_dialplan = dp


class DialplanLine(models.Model):
    _name = 'asterisk_base.dialplan_line'
    _order = 'sequence'
    _description = "Dialplan line"

    name = fields.Char(compute='_get_name')
    dialplan = fields.Many2one('asterisk_base.dialplan')
    exten = fields.Char()
    sequence = fields.Integer()
    app = fields.Char(required=True)
    app_data = fields.Char()
    label = fields.Char()

    def _get_name(self):
        for rec in self:
            rec.name = '{}({})'.format(rec.app, rec.app_data or '')
