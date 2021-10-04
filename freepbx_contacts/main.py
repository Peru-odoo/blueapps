# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import http, SUPERUSER_ID, registry
from odoo.api import Environment
from werkzeug.exceptions import Forbidden, Unauthorized
import uuid

logger = logging.getLogger(__name__)


class FreePBXContacts(http.Controller):
    @http.route('/freepbx_contacts', auth='none', type='json',
                methods=['GET'])
    def get_contacts(self):
        # Check auth token
        token = http.request.jsonrequest.get('token')
        if not token:
            raise Unauthorized('No auth token sent.')
        db = http.request.jsonrequest.get('db')
        if not db:
            raise Unauthorized('No db sent.')
        partners_list = []
        with registry(db).cursor() as cr:
            env = Environment(cr, SUPERUSER_ID, {})
            if token != env[
                    'ir.config_parameter'].get_param('freepbx.token'):
                raise Forbidden('Bad token!')
            partners = env['res.partner'].search(
                ['|', ('phone', 'not in', ['', False]),
                      ('mobile', 'not in', ['', False])])
            for p in partners:
                contact = {
                    'name': p.name,
                    'title': p.title.name,
                    'phone': p.phone,
                    'mobile': p.mobile,
                    'email': p.email,
                    'website': p.website,
                    'country': p.country_id.name,
                    'street': p.street,
                    'street2': p.street2,
                    'city': p.city,
                    'state': p.state_id.name,
                    'zip': p.zip,
                }
                partners_list.append(contact)
        return partners_list

    @http.route('/freepbx_contacts/init_cfg', auth='public', type='http',
                methods=['GET'])
    def init(self):
        if http.request.env[
                'ir.config_parameter'].sudo().get_param('freepbx.token'):
            raise Forbidden('Already initialized!')
        # No generate a token and save it.
        token = uuid.uuid4().hex
        http.request.env[
                'ir.config_parameter'].sudo().set_param('freepbx.token', token)
        # Create a config file.
        web_base_url = http.request.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
        db = http.request.env.registry.db_name
        cfg = """[odoo]
url={}
token={}
db={}

[mysql]
host=localhost
user=root
passwd=
db=asterisk
""".format(web_base_url, token, db)
        return cfg

    @http.route('/freepbx_contacts/install.sh', auth='public', type='http',
                methods=['GET'])
    def install(self):
        # TODO
        pass
