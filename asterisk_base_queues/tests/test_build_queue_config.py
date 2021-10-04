# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
from odoo.tests.common import TransactionCase


class QueueConfigTest(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.queue = self.env.ref('asterisk_base_queues.sales_queue')
        self.admin = self.env.ref('base.user_admin')
        self.demo = self.env.ref('base.user_demo')
        self.aster_admin = self.env.ref('asterisk_base_queues.user_admin')
        self.aster_demo = self.env.ref('asterisk_common.user_demo')
        self.server = self.env.ref('asterisk_base.default_server')
        return result

    def test_generic_queue_settings_all_true(self):
        self.maxDiff = None
        o = {
            'persistentmembers': True,
            'keepstats': True,
            'autofill': True,
            'autopause': True,
            'maxlen': 30,
            'setinterfacevar': True,
            'setqueueentryvar': True,
            'setqueuevar': True,
            'monitor_type': 'MixMonitor',
            'monitor_format': 'wav',
            'membermacro': 'X',
            'updatecdr': True,
            'shared_lastcall': True,
            'negative_penalty_invalid': True,
            'shared_lastcall': True,
            'negative_penalty_invalid': True,
            'log_membername_as_agent': True,
            'default_ring_timeout': 30,
            'default_queue_timeout': 30 
        }
        template = self.env['asterisk_base.conf_template'].render_template(
                'general_queue_settings', 
                vals={'rec': o},
                server_id=self.server.id
        )
        self.assertEqual(
                template,
                '[general](+)\n; Queue Settings\npersistentmembers=yes\n'
                'keepstats=yes\nautofill=yes\nautopause=yes\n'
                'maxlen=30\nsetinterfacevar=yes\nsetqueueentryvar=yes\n'
                'setqueuevar=yes\nmonitor_type=MixMonitor\nmonitor_format=wav\n'
                'membermacro=X\nupdatecdr=yes\nshared_lastcall=yes\n'
                'negative_penalty_invalid=yes\nlog_membername_as_agent=yes\n'
                'default_ring_timeout=30\ndefault_queue_timeout=30')

    def test_generic_queue_settings_all_false(self):
        self.maxDiff = None
        o = {
            'persistentmembers': False,
            'keepstats': False,
            'autofill': False,
            'autopause': False,
            'maxlen': 30,
            'setinterfacevar': False,
            'setqueueentryvar': False,
            'setqueuevar': False,
            'monitor_type': 'MixMonitor',
            'monitor_format': 'wav',
            'membermacro': 'X',
            'updatecdr': False,
            'shared_lastcall': False,
            'negative_penalty_invalid': False,
            'shared_lastcall': False,
            'negative_penalty_invalid': False,
            'log_membername_as_agent': False,
            'default_ring_timeout': 30,
            'default_queue_timeout': 30 
        }
        template = self.env['asterisk_base.conf_template'].render_template(
                'general_queue_settings', 
                vals={'rec': o},
                server_id=self.server.id
        )
        self.assertEqual(
                template,
                '[general](+)\n; Queue Settings\npersistentmembers=no\n'
                'keepstats=no\nautofill=no\nautopause=no\n'
                'maxlen=30\nsetinterfacevar=no\nsetqueueentryvar=no\n'
                'setqueuevar=no\nmonitor_type=MixMonitor\nmonitor_format=wav\n'
                'membermacro=X\nupdatecdr=no\nshared_lastcall=no\n'
                'negative_penalty_invalid=no\nlog_membername_as_agent=no\n'
                'default_ring_timeout=30\ndefault_queue_timeout=30')


    def test_queue_extension(self):
        o = {
            'name': 'testqueue',
            'timeout': 30,
            'options': 'test',
            'maxlen': 30
        }
        template = self.env['asterisk_base.conf_template'].render_template(
                'queue_extension', 
                vals={'rec': o},
                server_id=self.server.id
        )
        self.assertEqual(
            template, 
            'same => n,Answer()\nsame => n,Queue(testqueue,test,,,30)\n'
            'same => n,Playtones(busy)\nsame => n,Wait(11)\nsame => n,Hangup()\n'
        )
        o2 = o.copy()
        o2['continue_on_hangup']='true'
        template = self.env['asterisk_base.conf_template'].render_template(
                'queue_extension', 
                vals={'rec': o2},
                server_id=self.server.id
        )
        self.assertEqual(
            template, 
            'same => n,Answer()\nsame => n,Queue(testqueue,ctest,,,30)\n'
            'same => n,Playtones(busy)\nsame => n,Wait(11)\nsame => n,Hangup()\n'
        )
        o2['continue_exten']= {'number': 301}
        template = self.env['asterisk_base.conf_template'].render_template(
                'queue_extension', 
                vals={'rec': o2},
                server_id=self.server.id
        )
        self.assertEqual(
            template, 
            'same => n,Answer()\nsame => n,Queue(testqueue,ctest,,,30)\n'
            'same => n,GotoIf($["${QUEUESTATUS}" = "CONTINUE"]?continue)\n'
            'same => n,Playtones(busy)\nsame => n,Wait(11)\nsame => n,Hangup()\n'
            'same => n(continue),Verbose(QUEUESTATUS: CONTINUE)\nsame => n,Wait(1); Loop protection\n'
            'same => n,Goto(301,1)\n'
        )
        o3 = o.copy()
        o3['timeout_exten'] = {'number': 302}
        template = self.env['asterisk_base.conf_template'].render_template(
                'queue_extension', 
                vals={'rec': o3},
                server_id=self.server.id
        )
        self.assertEqual(
            template, 
            'same => n,Answer()\nsame => n,Queue(testqueue,test,,,30)\n'
            'same => n,GotoIf($["${QUEUESTATUS}" = "TIMEOUT"]?timeout)\n'
            'same => n,Playtones(busy)\nsame => n,Wait(11)\nsame => n,Hangup()\n'
            'same => n(timeout),Verbose(QUEUESTATUS: TIMEOUT)\nsame => n,Wait(1); Loop protection\n'
            'same => n,Goto(odoo-extensions, 302,1)\n'
        )

    def test_queue_template(self):
        o= {
            'name': 'Sales',
            'strategy': 'ringall',
            'ringinuse': True,
            'musicclass': 'default',
            'maxlen': 10,
            'servicelevel': 'test',
            'ring_timeout': 10,
            'reportholdtime': True,
            'leavewhenempty': True,
            'joinempty': True,
        }
        members = ['test{}'.format(x) for x in range(5)]
        template = self.env['asterisk_base.conf_template'].render_template(
            'queue', 
            vals={'rec': o, 'static_members': members},
            server_id=self.server.id
        )
        self.assertEqual(
            template,
            """;
[Sales]
strategy=ringall
ringinuse=yes
musicclass=default
maxlen=10
servicelevel=test
timeout=10
reportholdtime=yes
leavewhenempty=yes
joinempty=yes
; MEMBERS
member => test0
member => test1
member => test2
member => test3
member => test4
"""
        )


    def test_sales_queue_config(self):
        queue_config = self.env['asterisk_base.conf'].get_or_create(
            self.server.id, 'queues_odoo.conf'
        )
        self.maxDiff = None
        self.assertEqual(
            queue_config.content,
            '[general](+)\n; Queue Settings\npersistentmembers=no\n'
            'keepstats=no\nautofill=no\nautopause=yes\n'
            'maxlen=0\nsetinterfacevar=no\nsetqueueentryvar=no\n'
            'setqueuevar=no\nmonitor_type=mix_monitor\nmonitor_format=wav\n'
            'updatecdr=no\nshared_lastcall=yes\nnegative_penalty_invalid=no\n'
            'log_membername_as_agent=no\ndefault_ring_timeout=15\n'
            'default_queue_timeout=300\n;\n[Sales]\nstrategy=ringall\n'
            'announce-frequency=30\nringinuse=no\nmusicclass=default'
            '\nmaxlen=0\nservicelevel=60\ntimeout=15\nreportholdtime=no'
            '\nleavewhenempty=no\njoinempty=yes\n; MEMBERS\n')
        self.env['asterisk_base_queues.queue_member'].create({
            'user': self.aster_admin.id,
            'queue': self.queue.id,
            'is_static': True
        })
        self.assertEqual(
            queue_config.content,
            '[general](+)\n; Queue Settings\npersistentmembers=no\n'
            'keepstats=no\nautofill=no\nautopause=yes\nmaxlen=0\n'
            'setinterfacevar=no\nsetqueueentryvar=no\n'
            'setqueuevar=no\nmonitor_type=mix_monitor\n'
            'monitor_format=wav\nupdatecdr=no\nshared_lastcall=yes\n'
            'negative_penalty_invalid=no\nlog_membername_as_agent=no\n'
            'default_ring_timeout=15\ndefault_queue_timeout=300\n;\n'
            '[Sales]\nstrategy=ringall\nannounce-frequency=30\nringinuse=no\n'
            'musicclass=default\nmaxlen=0\nservicelevel=60\ntimeout=15\n'
            'reportholdtime=no\nleavewhenempty=no\njoinempty=yes\n; MEMBERS\n'
            'member => SIP/1001\n')
        self.env['asterisk_base_queues.queue'].create({
            'name': 'Sales2',
            'exten': 102
        })
        self.assertEqual(
            queue_config.content,
            '[general](+)\n; Queue Settings\npersistentmembers=no\n'
            'keepstats=no\nautofill=no\nautopause=yes\nmaxlen=0\n'
            'setinterfacevar=no\nsetqueueentryvar=no\n'
            'setqueuevar=no\nmonitor_type=mix_monitor\n'
            'monitor_format=wav\nupdatecdr=no\nshared_lastcall=yes\n'
            'negative_penalty_invalid=no\nlog_membername_as_agent=no\n'
            'default_ring_timeout=15\ndefault_queue_timeout=300\n;\n'
            '[Sales]\nstrategy=ringall\nannounce-frequency=30\nringinuse=no\n'
            'musicclass=default\nmaxlen=0\nservicelevel=60\ntimeout=15\n'
            'reportholdtime=no\nleavewhenempty=no\njoinempty=yes\n; MEMBERS\n'
            'member => SIP/1001\n;\n'
            '[Sales2]\n'
            'strategy=ringall\n'
            'announce-frequency=30\n'
            'ringinuse=no\n'
            'musicclass=default\n'
            'maxlen=0\n'
            'servicelevel=60\n'
            'timeout=15\n'
            'reportholdtime=no\n'
            'leavewhenempty=no\n'
            'joinempty=yes\n'
            '; MEMBERS\n'
        )

