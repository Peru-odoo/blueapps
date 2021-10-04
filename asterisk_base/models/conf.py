# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import base64
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from ..utils import get_default_server

logger = logging.getLogger(__name__)


class AsteriskConf(models.Model):
    _name = 'asterisk_base.conf'
    _description = 'Configuration Files'
    _rec_name = 'name'
    _order = 'name'

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, copy=False)
    server = fields.Many2one(comodel_name='asterisk_base.server',
                             default=get_default_server,
                             required=True, ondelete='cascade')
    content = fields.Text()
    is_updated = fields.Boolean(string=_('Updated'))
    sync_date = fields.Datetime(readonly=True)
    sync_uid = fields.Many2one('res.users', readonly=True, string='Sync by')
    version = fields.Integer(
        default=1, required=True, index=True, readonly=True)

    _sql_constraints = []

    @api.model
    def create(self, vals):
        if not self.env.context.get('conf_no_update'):
            vals['is_updated'] = True
        rec = super(AsteriskConf, self).create(vals)
        return rec

    @api.constrains('name', 'active')
    def check_name(self):
        for rec in self:
            existing = self.env[
                'asterisk_base.conf'].search(
                [('name', '=', rec.name), ('server', '=', rec.server.id)])
            if len(existing) > 1:
                raise ValidationError(
                    'This filename is already used!')

    def write(self, vals):
        if 'name' in vals:
            raise ValidationError(
                _('Rename not possible. Create a new file and copy & paste.'))
        no_update = vals.get(
            'content') and self.env.context.get('conf_no_update')
        if 'content' in vals and not no_update:
            vals['is_updated'] = True
        if 'content' in vals and 'version' not in vals and not no_update:
            # Inc version
            for rec in self:
                vals['version'] = rec.version + 1
                super(AsteriskConf, rec).write(vals)
        else:
            super(AsteriskConf, self).write(vals)
        return True

    def unlink(self):
        for rec in self:
            if not rec.active:
                super(AsteriskConf, rec).unlink()
            else:
                rec.active = False
                self.unlink_on_asterisk()
        return True

    def unlink_on_asterisk(self):
        names = self.mapped('name')
        servers = self.mapped('server')
        for server in servers:
            server.agent.notify(
                'asterisk.delete_config',
                names,
                status_notify_uid=self.env.uid)

    def refresh_button(self):
        return True

    def toggle_active(self):
        for rec in self:
            rec.write({
                'active': not rec.active,
                'is_updated': not rec.active,
            })

    @api.model
    def get_or_create(self, server_id, name, content=''):
        # First try to get existing conf
        conf = self.env['asterisk_base.conf'].search(
            [('server', '=', server_id), ('name', '=', name)])
        if not conf:
            # Create a new one
            data = {'server': server_id, 'name': name, 'content': content}
            conf = self.env['asterisk_base.conf'].create(data)
        return conf

    def include_from(self, from_name):
        self.ensure_one()
        from_conf = self.env['asterisk_base.conf'].search(
            [('name', '=', from_name), ('server', '=', self.server.id)])
        if not from_conf or not from_conf.content:
            logger.warning(
                'File %s not found or empty, ignoring #tryinclude.', from_name)
            return
        # Check if include is already there.
        conf_basename = from_name.split('.')[0]
        include_string = '#tryinclude {}_odoo*.conf'.format(conf_basename)
        if (include_string not in from_conf.content):
            from_conf.content += '\n{}\n'.format(include_string)

    def upload_conf(self):
        # Upload conf to server
        self.ensure_one()
        self.server.agent.notify(
            'asterisk.put_config',
            self.name,
            base64.b64encode(self.content.encode()).decode(),
            callback=('asterisk_base.conf', 'upload_conf_response'),
            passback={
                'res_id': self.id,
                'uid': self.env.uid,
                'name': self.name,
            })

    @api.model
    def upload_conf_response(self, response):
        if response.get('error'):
            logger.warning('Upload conf error: %s', response)
            self.env.user.asterisk_notify(
                'File {} error: {}'.format(
                    response['passback']['name'],
                    response['error']['message']),
                uid=response['passback']['uid'])
            return False
        conf = self.browse(response['passback']['res_id'])
        conf.write({
            'is_updated': False,
            'sync_date': fields.Datetime.now(),
            'sync_uid': response['passback']['uid']
        })
        self.env.user.asterisk_notify(
            'File {} uploaded.'.format(response['passback']['name']),
            uid=response['passback']['uid'])
        return True

    def download_conf(self, notify_uid=None):
        self.ensure_one()
        self.server.agent.notify(
            'asterisk.get_config',
            self.name,
            callback=('asterisk_base.conf', 'download_conf_response'),
            passback={
                'res_id': self.id,
                'uid': self.env.uid,
                'name': self.name,
            })

    @api.model
    def download_conf_response(self, response):
        if response.get('error'):
            logger.warning('Download conf error: %s', response)
            self.env.user.asterisk_notify(
                'File {} error: {}'.format(
                    response['passback']['name'],
                    response['error']['message']),
                uid=response['passback']['uid'])
            return False
        conf = self.browse(response['passback']['res_id'])
        conf.with_context({'conf_no_update': True}).write({
            'content': base64.b64decode(
                response['result']['file_data'].encode()).decode('latin-1'),
            'sync_date': fields.Datetime.now(),
            'sync_uid': self.env.user.id})
        self.env.user.asterisk_notify(
            'File {} downloaded.'.format(response['passback']['name']),
            uid=response['passback']['uid'])
        # TODO: Reload file form.
        return True
