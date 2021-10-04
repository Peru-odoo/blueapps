# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
from odoo.tests import common
from odoo.tests import tagged
from odoo.exceptions import ValidationError
from odoo.addons.asterisk_base.models.server import AsteriskServer

import logging

logger = logging.getLogger(__name__)


class TestExtension(common.TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.default_server = self.env.ref('asterisk_base.default_server')
        # We take server for object as we does not care here really.
        self.extension = self.env['asterisk_base.extension'].with_context(
            {'no_build_conf': True}).create({
                'server': self.default_server.id,
                'number': '100',
                'app': 'asterisk_base',
                'model': 'user',
                'obj_id': self.default_server.id,
            })
        return result

    def test_render_server_template(self):
        """Test for server extension object"""
        ext = self.env['asterisk_base.extension'].browse(self.extension.id)
        base_conf = self.env['asterisk_base.conf_template'].render_template(
            'extension_base',
            server_id=self.default_server.id,
            vals={'object': ext}
        )
        dialplan_conf = self.env['asterisk_base.conf_template'].render_template(
            'extension_dialplan',
            server_id=self.default_server.id,
            vals={'object': ext}
        )
        self.assertEqual(
            '; Extension for '
            '{}\n\n    exten => {},1,Verbose(EXTENSION {})\n'.format(
                ext.name, ext.number, ext.name),
            base_conf)
        self.assertEqual(
            '\n    exten => ,n,Goto(dialplan-{},${{EXTEN}},1)\n'.format(ext.id),
            dialplan_conf)

    def test_render_server_template_with_record(self):
        """Test for server extension object"""
        ext = self.env['asterisk_base.extension'].browse(self.extension.id)
        ext.record_calls = True
        base_conf = self.env['asterisk_base.conf_template'].render_template(
            'extension_base',
            server_id=self.default_server.id,
            vals={'object': ext}
        )
        dialplan_conf = self.env['asterisk_base.conf_template'].render_template(
            'extension_dialplan',
            server_id=self.default_server.id,
            vals={'object': ext}
        )
        self.assertEqual(
            '; Extension for '
            '{}\n\n    exten => {},1,MixMonitor(${{UNIQUEID}}.wav)\n'.format(
                ext.name, ext.number),
            base_conf)
        self.assertEqual(
            '\n    exten => ,n,Goto(dialplan-{},${{EXTEN}},1)\n'.format(ext.id),
            dialplan_conf)

    def test_render_dialplan_template_with_custom(self):
        """Test for server extension object"""
        dialplan = self.env.ref('asterisk_base.simple_dialplan')
        ext = self.env['asterisk_base.extension'].with_context(
            {'no_build_conf': True}).create({
                'server': self.default_server.id,
                'number': '101',
                'app': 'asterisk_base',
                'model': 'dialplan',
                'obj_id': dialplan.id,
                'record_calls': False
            })
        dialplan.extension = ext
        dialplan.write({
            'is_custom': True,
        })
        base_conf = self.env['asterisk_base.conf_template'].render_template(
            'extension_base',
            server_id=self.default_server.id,
            vals={'object': ext, 'rec': self}
        )
        dialplan_conf = self.env['asterisk_base.conf_template'].render_template(
            'extension_dialplan',
            server_id=self.default_server.id,
            vals={'object': dialplan}
        )
        self.assertEqual(
            '; Extension for '
            '{}\n\n    exten => {},1,Verbose(EXTENSION Test Dialplan)\n'.format(
                ext.name, ext.number),
            base_conf)
        self.assertEqual(
            '\n    exten => {},n,Goto(dialplan-{},${{EXTEN}},1)\n'.format(
                dialplan.exten, dialplan.id),
            dialplan_conf)
