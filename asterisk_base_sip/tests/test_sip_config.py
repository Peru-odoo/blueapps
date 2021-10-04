# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
from odoo.tests.common import TransactionCase


class SipTemplateTest(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.admin = self.env.ref('base.user_admin')
        self.demo = self.env.ref('base.user_demo')
        self.server = self.env.ref('asterisk_base.default_server')
        self.maxDiff = None
        return result

    def test_sip_peer(self):
        params = ['note', 'accountcode', 'disallow', 'allow',
            'allowoverlap', 'allowtransfer', 'allowsubscribe', 'amaflags',
            'autoframing', 'avpf', 'buggymwi', 'busylevel', 'callbackextension',
            'callcounter', 'callgroup', 'callingpres', 'callerid',
            'canreinvite', 'cancallforward', 'context', 'contactacl',
            'contactdeny', 'contactpermit', 'defaultip', 'defaultuser',
            'deny', 'dtlsautogeneratecert', 'dtlscafile', 'dtlscertfile',
            'dtlscipher', 'dtlsenable', 'dtlsfingerprint', 'dtlssetup',
            'dtlsverify', 'directmedia', 'dtmfmode', 'faxdetect',
            'force_avp', 'fromdomain', 'fromuser', 'g726nonstandard',
            'host', 'ignoresdpversion', 'insecure', 'icesupport',
            'language', 'mailbox', 'mask', 'maxcallbitrate', 
            'md5secret', 'mohinterpret', 'mohsuggest', 'musiconhold', 'nat',
            'outboundproxy', 'parkinglot', 'permit', 'pickupgroup', 'port',
            'progressinband', 'qualify', 'qualifyfreq', 'regcontext', 'regexten',
            'remotesecret', 'remotesecret', 'rfc2833compensate', 'rtcp_mux',
            'rtpholdtimeout', 'rtpkeepalive', 'rtptimeout', 'secret', 'sendrpid',
            'srvlookup', 'subscribecontext', 'subscribemwi', 'supportpath',
            't38pt_usertpsource', 'textsupport', 'timerb', 'timert1', 
            'transport', 'trustrpid', 'type', 'usereqphone', 'videosupport',
            'vmexten']

        rec = {
            'name': 'test_peer',
            'channel_vars': ['channel_var1', 'channel_var2'],
            'template': {'name': 'Test template'}
        }
        for param in params:
            rec[param] = 'test_'+param
        template = self.env['asterisk_base.conf_template'].render_template(
            'sip_peer',
            vals={'rec': rec},
            server_id=self.server.id
        )
        self.assertEqual(
            template,
            ''';
[test_peer](test_template); test_note 
accountcode=test_accountcode
disallow=test_disallow
allow=test_allow
allowoverlap=test_allowoverlap
allowtransfer=test_allowtransfer
allowsubscribe=test_allowsubscribe
amaflags=test_amaflags
autoframing=test_autoframing
avpf=test_avpf
buggymwi=test_buggymwi
busylevel=test_busylevel
callbackextension=test_callbackextension
callcounter=test_callcounter
callgroup=test_callgroup
callingpres=test_callingpres
callerid=test_callerid
canreinvite=test_canreinvite
cancallforward=test_cancallforward
context=test_context
contactacl=test_contactacl
contactdeny=test_contactdeny
contactpermit=test_contactpermit
defaultip=test_defaultip
defaultuser=test_defaultuser
deny=test_deny
dtlsautogeneratecert=test_dtlsautogeneratecert
dtlscafile=test_dtlscafile
dtlscertfile=test_dtlscertfile
dtlscipher=test_dtlscipher
dtlsenable=test_dtlsenable
dtlsfingerprint=test_dtlsfingerprint
dtlssetup=test_dtlssetup
dtlsverify=test_dtlsverify
directmedia=test_directmedia
dtmfmode=test_dtmfmode
faxdetect=test_faxdetect
force_avp=test_force_avp
fromdomain=test_fromdomain
fromuser=test_fromuser
g726nonstandard=test_g726nonstandard
host=test_host
ignoresdpversion=test_ignoresdpversion
insecure=test_insecure
icesupport=test_icesupport
language=test_language
mailbox=test_mailbox
mask=test_mask
maxcallbitrate=test_maxcallbitrate
md5secret=test_md5secret
mohinterpret=test_mohinterpret
mohsuggest=test_mohsuggest
musiconhold=test_musiconhold
nat=test_nat
outboundproxy=test_outboundproxy
parkinglot=test_parkinglot
permit=test_permit
pickupgroup=test_pickupgroup
port=test_port
progressinband=test_progressinband
qualify=test_qualify
qualifyfreq=test_qualifyfreq
regcontext=test_regcontext
regexten=test_regexten
remotesecret=test_remotesecret
rfc2833compensate=test_rfc2833compensate
rtcp_mux=test_rtcp_mux
rtpholdtimeout=test_rtpholdtimeout
rtpkeepalive=test_rtpkeepalive
rtptimeout=test_rtptimeout
secret=test_secret
sendrpid=test_sendrpid
srvlookup=test_srvlookup
subscribecontext=test_subscribecontext
subscribemwi=test_subscribemwi
supportpath=test_supportpath
t38pt_usertpsource=test_t38pt_usertpsource
textsupport=test_textsupport
timerb=test_timerb
timert1=test_timert1
transport=test_transport
trustrpid=test_trustrpid
type=test_type
usereqphone=test_usereqphone
videosupport=test_videosupport
vmexten=test_vmexten\n''')

    def test_sip_peer_template(self):
        rec = {
            'section_name': 'test_template',
            'common_options': [
                {'param': 'option1', 'value': "test1"},
                {'param': 'option2', 'value': "test2"},
                {'param': 'option3', 'value': "test3"},
            ]
        }
        template = self.env['asterisk_base.conf_template'].render_template(
                'sip_template', 
                vals={'rec': rec},
                server_id=self.server.id
        )
        self.assertEqual(
            template,
            ';\n[test_template](!)\noption1=test1\noption2=test2\n'
            'option3=test3\n'
        )
        rec['note'] = 'test_note'
        template = self.env['asterisk_base.conf_template'].render_template(
                'sip_template',
                vals={'rec': rec},
                server_id=self.server.id
        )
        self.assertEqual(
            template,
            ';\n[test_template](!); test_note\noption1=test1\noption2=test2\n'
            'option3=test3\n'
        )
