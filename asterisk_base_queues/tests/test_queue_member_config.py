# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.addons.asterisk_common.models.res_users import ResUser
from odoo.addons.asterisk_common.models.agent import Agent
from odoo.addons.asterisk_base.models.extension import Extension

from unittest.mock import patch, call
from ..models.queue import Queue
from ..models.queue_member import QueueMember

import logging

logger = logging.getLogger(__name__)


class TestOperators(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.queue = self.env.ref('asterisk_base_queues.sales_queue')
        self.admin = self.env.ref('base.user_admin')
        self.demo = self.env.ref('base.user_demo')
        self.aster_admin = self.env.ref('asterisk_base_queues.user_admin')
        self.aster_demo = self.env.ref('asterisk_common.user_demo')
        self.QueueMember = self.env['asterisk_base_queues.queue_member']
        return result

    def test_static_operator(self):
        """Check static operator creation and removal"""
        with patch.object(Queue, 'build_conf') as m_queue_build_conf, \
                patch.object(Extension, 'build_conf') as m_ext_build_conf:
            test = self.QueueMember.create({
                'user': self.aster_admin.id,
                'queue': self.queue.id,
                'is_static': True
            })
            self.assertEqual(test.user, self.aster_admin)
            self.assertEqual(test.queue, self.queue)
            m_queue_build_conf.assert_called_once()
            m_ext_build_conf.assert_called_once()

        with patch.object(QueueMember, 'send_queue_leave_request') as m_leave:
            test.unlink()
            m_leave.assert_not_called()

    def test_dynamic_operator(self):
        """Check dynamic operator creation and removal"""
        with patch.object(Queue, 'build_conf') as m_queue_build_conf, \
                patch.object(Extension, 'build_conf') as m_ext_build_conf:
            test = self.QueueMember.create({
                'user': self.aster_admin.id,
                'queue': self.queue.id,
                'is_static': False
            })
            self.assertEqual(test.user, self.aster_admin)
            self.assertEqual(test.queue, self.queue)
            m_queue_build_conf.assert_not_called()
            m_ext_build_conf.assert_called_once()

        with patch.object(QueueMember, 'send_queue_leave_request') as m_leave:
            test.unlink()
            m_leave.assert_called_once()

    def test_static_no_queue_interface(self):
        """Raise ValidationError when trying to create static queue members"""
        with self.assertRaises(ValidationError):
            self.QueueMember.with_context(no_build_conf=True).create({
                'user': self.aster_demo.id,
                'queue': self.queue.id,
                'is_static': True
            })

    def test_queue_leave_request(self):
        """Makes sure that queue_leave_request is being sent"""
        test = self.QueueMember.create({
            'user': self.aster_admin.id,
            'queue': self.queue.id,
            'is_static': False
        })
        with patch.object(Agent, 'notify') as mock_notify:
            test.send_queue_leave_request()
            mock_notify.assert_called_once()
            mock_notify.assert_has_calls([
                call('asterisk', {
                    'command': 'execute',
                    'system_name': 'asterisk',
                    'method': 'asterisk.send_ami_action',
                    'callback_model': 'asterisk_base_queues.queue',
                    'callback_method': 'leave_response',
                    'args': [{
                        'Action': 'QueueRemove',
                        'Queue': self.queue.name,
                        'Interface': self.aster_admin.queue_interface
                    }],
                    'pass_back': {
                        'uid': self.env.user.id,
                        'queue': self.queue.id,
                        'asterisk_user': self.aster_admin.id
                    }})])
