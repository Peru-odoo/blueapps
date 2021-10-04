# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import difflib
from jinja2.sandbox import SandboxedEnvironment
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import ustr
from ..utils import get_default_server


logger = logging.getLogger(__name__)


class ConfTemplate(models.Model):
    _name = 'asterisk_base.conf_template'
    _description = 'Asterisk Base Config Template'
    _order = 'name'

    name = fields.Char(required=True, copy=False)
    code = fields.Char(required=True)
    server = fields.Many2one(comodel_name='asterisk_base.server', required=True,
                             ondelete='cascade', default=get_default_server)
    content = fields.Text(required=True)
    original_content = fields.Text(readonly=True)
    diff_content = fields.Text(compute='_get_diff_content')

    _sql_constraints = [
        ('code_uniq', 'UNIQUE(code,server)', 'This template code is already used!')
    ]


    def _strip_empty_lines(self, content):
        # Remove empty lines
        lines = []
        if not content:
            content = ''
        for line in content.split('\n'):
            if line.strip(' '):
                lines.append(line)
        return '\n'.join(lines)

    @api.model
    def create(self, vals):
        # Remove empty lines        
        vals['content'] = self._strip_empty_lines(vals.get('content'))
        # Store a copy of original content.
        vals['original_content'] = vals['content']
        return super(ConfTemplate, self).create(vals)

    def write(self, vals):
        if self.env.context.get('install_mode') or self.env.context.get(
                'module') == 'asterisk_base':
            vals['original_content'] = self._strip_empty_lines(
                vals.get('content'))
            # Do not update the current content!
            del vals['content']
        return super(ConfTemplate, self).write(vals)

    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('code', '=like', "{}-%".format(self.name))])
        if not copied_count:
            new_code = "{}-1".format(self.code)
        else:
            new_code = "{}-{}".format(self.code, copied_count+1)
        default['code'] = new_code
        return super(ConfTemplate, self).copy(default)

    def render(self, vals):
        self.ensure_one()
        template_env = SandboxedEnvironment(
            lstrip_blocks=True,
            keep_trailing_newline=True,
            trim_blocks=False, # Otherwise inline statesments trim newline.
            autoescape=False
        )
        template = template_env.from_string(ustr(self.content))
        result = template.render(vals)
        return result

    @api.model
    def render_template(self, code, server_id, vals):
        # Used in other modules to shortify template search and render.
        t = self.search([('code', '=', code), ('server', '=', server_id)])
        if not t:
            raise ValidationError(
                'Config template with code {} does '
                'not exist on server ID {}!'.format(code, server_id))
        return t.render(vals)

    def _get_diff_content(self):
        for rec in self:
            rec.diff_content = '\n'.join(difflib.unified_diff(
                rec.original_content.split('\n'),
                rec.content.split('\n'),
                fromfile='original',
                tofile='current'))

    def upgrade(self):
        # For now just override. TODO: smart merge.
        for rec in self:
            rec['content'] = rec['original_content']
