# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
# -*- encoding: utf-8 -*-
from ast import literal_eval
import base64
from datetime import datetime, timedelta
from jinja2.sandbox import SandboxedEnvironment
import json
import logging
from urllib.parse import unquote
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger, ustr
from psycopg2 import IntegrityError

from .campaign_log import LOG_LEVELS

logger = logging.getLogger(__name__)

CAMPAIGN_STATES = [
    ('new', 'New'),
    ('running', 'Running'),
    ('paused', 'Paused'),
    ('done', 'Done')
]

CAMPAIGN_TYPES = [
    ('operators', 'Operators'),
    ('voice_message', 'Voice Message')
]

MESSAGE_TYPES = [
    ('sound_file', 'Sound File'),
    ('google_tts', 'Google TTS')
]


def convert_agi_env(env):
    # Function to unquote AGI Env
    res = dict()
    res.update([k.split(': ') for k in unquote(env).split('\n') if k])
    return res


class Campaign(models.Model):
    _name = 'asterisk_dialer.campaign'
    _description = _('Dialer Campaign')

    name = fields.Char(required=True, help=_("A descriptive name."))
    number = fields.Char(help=_("An extension number to dial to begin outbound calling."
                                "\nAsterisk must execute AGI(agi:async) when dialed."))
    campaign_type = fields.Selection(
        CAMPAIGN_TYPES,
        required=True,
        default='operators',
        help=_("Operators: an operator dials the number to begin outbound calling.\n"
               "Voice Message: play a voice message to all contacts."),
    )
    start_type = fields.Selection(
        [('manual', 'Manual'), ('scheduled', 'Scheduled'),
         ('periodic', 'Periodic')], default='manual', required=True,
        help=_('Manual: run manually'
               '\nScheduled: specify start and end time'
               '\nPeriodic: run periodically in a given time')
    )
    # Periodic settings
    period_type = fields.Selection(
        [('hours', 'Hours'), ('days', 'Days'),
         ('weeks', 'Weeks')], default='days',
    )
    period_number = fields.Integer(
        default='1',
    )
    next_run = fields.Datetime(help=_("Select the starting point for the campaign."))
    channel_provider = fields.Char(
        required=True,
        default=lambda self: self.env['asterisk_common.settings'].get_param('default_provider'),
        help=_("Asterisk dialstring in Technology/Resource format."
               "\nString {NUMBER} is replaced with contact's phone number. Examples:"
               "\nSIP/{NUMBER}@sip.example.com"
               "\nPJSIP/{NUMBER}@sip.example.com"
               "\nIAX2/iax.examle.com/{NUMBER}"
               "\nLocal/{NUMBER}@example-context/n")
    )
    contacts = fields.One2many(
        'asterisk_dialer.contact',
        inverse_name='campaign',
        help=_("The list of contacts belonging to the campaign.")
    )
    contact_count = fields.Integer(
        compute='_get_contact_count', string='Contacts',
        help=_("Number of contacts in the campaign.")
    )
    call_count = fields.Integer(
        compute='_get_call_count', string='Calls',
        help=_("Number of calls in the campaign.")
    )
    log_count = fields.Integer(
        compute='_get_log_count', string='Logs',
        help=_("Number of campaign log entries.")
    )
    state = fields.Selection(CAMPAIGN_STATES, default='new')
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    dial_attempts = fields.Integer(
        default=lambda self: self.env['asterisk_common.settings'].get_param('dial_attempts'),
        help=_("Total dial attempts. Set more than one to re-dial if not answered.")
    )
    originate_timeout = fields.Integer(
        default=lambda self: self.env['asterisk_common.settings'].get_param('originate_timeout'),
        help=_("How many seconds to wait for an answer before considering noanswer.")
    )
    max_parallel_calls = fields.Integer(default=1)
    msg_type = fields.Selection(MESSAGE_TYPES, string='Message Type')
    msg_file = fields.Binary(string='Message File')
    playback_widget = fields.Char(compute='_get_playback_widget',
                                  string='Playback')
    msg_filename = fields.Char()
    # Google TTS fields
    tts_text = fields.Text(string='Message Text')
    tts_language = fields.Char('Language', default='en-US')
    tts_voice = fields.Char('Voice', default='en-US-Wavenet-A')
    tts_pitch = fields.Float('Pitch', default=0.0)
    tts_speaking_rate = fields.Float('Speaking Rate', default=1.0)
    # Special field to easily get if we should render message for each contact
    # or one message for all is fine. Depends on using variable substitutions.
    tts_is_common = fields.Boolean(compute='_compute_tts_is_common')
    #
    log_level = fields.Selection(
        LOG_LEVELS, default='i', required=True,
        help=_("Default is info. Use debug log level if more information is needed ")
    )
    logs = fields.One2many('asterisk_dialer.campaign_log', 'campaign')
    calls = fields.One2many('asterisk_dialer.channel', 'campaign', context={'active_test': False})
    domain = fields.Char(default="[('phone', '!=', False)]")
    model = fields.Char(default='res.partner')
    active = fields.Boolean(default=True, index=True)
    is_common_tts_created = fields.Boolean()

    _sql_constraints = [
        ('number_uniq', 'UNIQUE(number)',
            _('This campain number is already used'))
    ]

    def write(self, vals):
        self.log(content=[self, vals, ['state']])
        res = super(Campaign, self).write(vals)
        return res

    def _get_playback_widget(self):
        file_source = 'msg_file'
        for rec in self:
            rec.playback_widget = '<audio id="sound_file" preload="auto" ' \
                                  'controls="controls"> ' \
                                  '<source src="/web/content?model=asterisk_dialer.campaign&' \
                                  'id={recording_id}&filename={filename}&field={source}&' \
                                  'filename_field=msg_filename&download=True" />' \
                                  '</audio>'.format(
                                                    recording_id=rec.id,
                                                    filename=rec.msg_filename,
                                                    source=file_source)

    @api.constrains('start_date', 'end_date')
    def _check_start_date(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("Campaign end date must be greater then start date")

    @api.onchange('period_type', 'period_number')
    def _reset_next_run(self):
        self.next_run = datetime.now() + timedelta(
            **{self.period_type: self.period_number})

    @api.onchange('campaign_type')
    def _set_msg_type(self):
        if not self.msg_type:
            self.msg_type = 'sound_file'

    def _get_contact_count(self):
        for rec in self:
            rec.contact_count = self.env['asterisk_dialer.contact'].search_count(
                [('campaign', '=', rec.id)])

    def _get_call_count(self):
        for rec in self:
            rec.call_count = self.env['asterisk_dialer.channel'].search_count(
                [('campaign', '=', rec.id), ('active', 'in', [True, False])])

    def _get_log_count(self):
        for rec in self:
            rec.log_count = self.env['asterisk_dialer.campaign_log'].search_count(
                [('campaign', '=', rec.id)])

    def _compute_tts_is_common(self):
        for rec in self:
            if isinstance(rec.tts_text, str) and '{' in rec.tts_text:
                rec.tts_is_common = False
            else:
                rec.tts_is_common = True

    def render_voice_message(self, contact):
        # Helper function to render the message from template.
        try:
            template_env = SandboxedEnvironment(
                lstrip_blocks=True,
                trim_blocks=False,
                keep_trailing_newline=True,
                autoescape=False,
            )
            template = template_env.from_string(ustr(self.tts_text))
            text = template.render({
                'campaign': self,
                'contact': contact,
                'object': contact.model_object,
            })
        except Exception as e:
            raise ValidationError('Render error: {}'.format(e))
        # One message for all
        if self.tts_is_common:
            filename = 'odoo/dialer_campaign_{}'.format(self.id)
        else:
            filename = 'odoo/dialer_campaign_{}_contact_{}'.format(
                self.id, contact.id)
        # Generate sound file
        self.env.user.asterisk_agent.request(
            'asterisk.tts_create_sound',
            filename,
            text,
            self.tts_language,
            self.tts_voice,
            self.tts_pitch,
            self.tts_speaking_rate
        )

    def originate_to_contact(self, contact):
        # Is it voice message campaign?
        if contact.campaign.campaign_type == 'voice_message':
            # Render individual messages
            if not self.tts_is_common:
                self.render_voice_message(contact)
            # Render common message
            elif not self.is_common_tts_created:
                self.render_voice_message(contact)
                # Permission issues without sudo
                self.sudo().is_common_tts_created = True
        self.log('Originate to contact ID {} number {}'.format(
            contact.id, contact.phone), level='debug')
        # Originate to contact
        self.env['asterisk_dialer.channel'].originate(
            channel=contact.campaign.channel_provider.replace(
                '{NUMBER}', contact.phone),
            app='AGI',
            data='agi:async',
            campaign=self,
            contact=contact,
        )

    def check_campaign(self):
        # Check campaign status and dates
        if self.state != 'running':
            return False
        if self.end_date and (fields.Datetime.now() >= self.end_date):
            # Change campaign status to done
            self.state = 'done'
            return False
        return True

    def wakeup(self):
        self.ensure_one()
        self.log('Campaign {} wakeup.'.format(self.name), level='debug')
        if not self.check_campaign():
            return False
        # Get available operators
        operators_available = self.campaign_type == 'operators' and \
            self.get_available_operators() or []
        # Do we have a free operator?
        if self.campaign_type != 'operators' or operators_available:
            # Get current active calls
            current_calls = self.env['asterisk_dialer.channel'].search_count(
                [('campaign', '=', self.id),
                 ('active', '=', True),
                 ('contact', '!=', False)])
            # Check if we have available channels to originate.
            if self.max_parallel_calls <= current_calls:
                self.log('Max parallel calls reached.', level='debug')
                return False
            # Originate as much calls as is possible
            for i in range(0, self.max_parallel_calls - current_calls):
                contact = self.get_next_contact()
                if contact:
                    self.originate_to_contact(contact)
                else:
                    self.log('No more contacts to dial.', level='info')
                    # FIXME: Does not work.
                    # Remove non-working code.
        else:
            self.log('No available operators.', level='debug')

    def get_next_contact(self):
        contact = self.env['asterisk_dialer.contact'].search([
            '&', ('campaign', '=', self.id),
            '|', ('state', '=', 'q'),
            '&', ('state', '=', 'f'), ('dial_attempt', '<', self.dial_attempts)
        ], limit=1)
        if contact:
            contact.campaign.log('Got next contact to dial: {} - {}'.format(
                                 contact.name, contact.phone), level='debug')
            contact.write({
                'state': 'p',
                'dial_attempt': contact.dial_attempt + 1
            })
            self.env.cr.commit()
        return contact

    def get_available_operators(self):
        self.ensure_one()
        # Get campaign operators
        operators = self.env['asterisk_dialer.operator'].search(
            [('campaign', '=', self.id),
             ('state', '=', 'available')])
        logger.info('GET AVAILABLE OPERATORS: %s', ','.join(
            [k.name for k in operators]))
        return operators

    def connect_to_operator(self, channel):
        operators = self.get_available_operators()
        logger.info('CONNECT TO AVAILABLE OPERATORS: %s', ','.join(
            [k.name for k in operators]))
        # Connect to the operator
        if operators:
            operators[0].notify_operator({'contact': channel.contact.id})
            self.env.user.asterisk_agent.action({
                'Action': 'AGI',
                'Channel': channel.channel,
                'Command': 'EXEC ConfBridge {}'.format(operators[0].accountcode),
            }, notify=True, no_wait=True, as_list=False)
        else:
            self.log('NO AVAILABLE OPERATORS.', level='debug')

    def connect_to_voice_message(self, channel):
        # Originate a call to playback it
        if self.msg_type == 'sound_file' or self.tts_is_common:
            filename = 'odoo/dialer_campaign_{}'.format(self.id)
        else:
            filename = 'odoo/dialer_campaign_{}_contact_{}'.format(
                self.id, channel.contact.id)
        channel_name = channel.channel
        self.env.user.asterisk_agent.action({
            'Action': 'AGI',
            'Channel': channel_name,
            'Command': 'EXEC Wait 0.5'.format(filename),
        }, notify=True, no_wait=True, as_list=False)
        self.env.user.asterisk_agent.action({
            'Action': 'AGI',
            'Channel': channel_name,
            'Command': 'EXEC Playback {}'.format(filename),
        }, notify=True, no_wait=True, as_list=False)
        self.env.user.asterisk_agent.action({
            'Action': 'AGI',
            'Channel': channel_name,
            'Command': 'HANGUP {}'.format(channel_name),
        }, notify=True, no_wait=True, as_list=False)

    @api.model
    def async_agi_start(self, event):
        logger.info('AGI start: %s', json.dumps(event, indent=2))
        # Get the campaign by exten called by operator
        channel = self.env['asterisk_dialer.channel'].search(
            [('uniqueid', '=', event['Uniqueid'])])
        if not channel:
            # Now check if it is dialer app channel so that other apps channels
            # don't come here. Contact channels are pre-created so are found.
            # Operator channels are matched by accountcode.
            operator = self.env['asterisk_dialer.operator'].search(
                [('accountcode', '=', event['AccountCode'])])
            if not operator:
                logger.warning('OPERATOR NOT FOUND BY ACCOUNTCODE %s!',
                               event['AccountCode'])
                self.env.user.asterisk_agent.action({
                    'Action': 'Hangup',
                    'Channel': event['Channel']
                }, no_wait=True, notify=True)
                return False
            campaign = self.search([('number', '=', event['Exten'])])
            if not campaign:
                logger.warning(
                    'OPERATOR CAMPAIGN NOT FOUND BY NUMBER %s', event['Exten'])
                self.env.user.asterisk_agent.action({
                    'Action': 'Hangup',
                    'Channel': event['Channel']
                }, no_wait=True, notify=True)
                return False
            # Operator & campaign found, log a message and create the channel.
            campaign.log('OPERATOR {} FOUND.'.format(operator.name),
                         level='debug')
            # Create the channel for operator
            self.env['asterisk_dialer.channel'].create({
                'operator': operator.id,
                'campaign': campaign.id,
                'system_name': event.get('SystemName', ''),
                'channel': event.get('Channel', ''),
                'callerid_num': event.get('CallerIDNum', ''),
                'callerid_name': event.get('CallerIDName', ''),
                'connected_line_num': event.get('ConnectedLineNum', ''),
                'connected_line_name': event.get('ConnectedLineName', ''),
                'state': event.get('ChannelState', ''),
                'state_desc': event.get('ChannelStateDesc', ''),
                'uniqueid': event.get('Uniqueid', ''),
                'linkedid': event.get('Linkedid', ''),
                'context': event.get('Context', ''),
                'exten': event.get('Exten', ''),
                'accountcode': event.get('AccountCode', ''),
                'priority': event.get('Priority', ''),
            })
            # Update operator's state.
            operator.write({
                'state': 'available',
                'channel': event['Channel'],
                'campaign': campaign.id
            })
            self.env.cr.commit()
            # Answer the channel
            self.env.user.asterisk_agent.action({
                'Action': 'AGI',
                "Command": "Answer",
                'Channel': event.get('Channel')},
                notify=True, no_wait=True, as_list=False)
            # Add to the operator's confbridge.
            self.env.user.asterisk_agent.action({
                'Action': 'AGI',
                'Channel': event.get('Channel'),
                'Command': 'EXEC ConfBridge {}'.format(
                    operator.accountcode),
            }, notify=True, no_wait=True, as_list=False)
            return True
        # Check if this is a contact call.
        elif channel and channel.contact:
            channel.write({
                'channel': event.get('Channel', ''),
                'callerid_num': event.get('CallerIDNum', ''),
                'callerid_name': event.get('CallerIDName', ''),
                'connected_line_num': event.get('ConnectedLineNum', ''),
                'connected_line_name': event.get('ConnectedLineName', ''),
                'state': event.get('ChannelState', ''),
                'state_desc': event.get('ChannelStateDesc', ''),
                'uniqueid': event.get('Uniqueid', ''),
                'linkedid': event.get('Linkedid', ''),
                'context': event.get('Context', ''),
                'exten': event.get('Exten', ''),
                'accountcode': event.get('AccountCode', ''),
                'priority': event.get('Priority', ''),
            })
            camp = channel.campaign
            if camp.campaign_type == 'operators':
                camp.connect_to_operator(channel)
            elif camp.campaign_type == 'voice_message':
                camp.connect_to_voice_message(channel)
            return True
        else:
            logger.warning('AGI START NOT HANDLED.')
            return False

    def run_campaign(self):
        self.state = 'running'
        self.wakeup()

    def pause_campaign(self):
        self.state = 'paused'

    def done_campaign(self):
        self.state = 'done'
        # Delete common sound file
        if self.tts_is_common:
            filename = 'dialer_campaign_{}.wav'.format(
                self.id)
            self.env.user.asterisk_agent.request(
                'asterisk.delete_prompt',
                filename
            )
        self.is_common_tts_created = False

    def generate_contacts(self, model, domain):
        if isinstance(domain, str):
            domain = literal_eval(domain)
        contacts = self.env[model].search(domain)
        # Save current domain and model for campaign
        self.write({'domain': domain, 'model': model})
        # Get origination settings
        originate_format = self.env['asterisk_common.settings'].sudo(
            ).get_param('originate_format')
        originate_prefix = self.env['asterisk_common.settings'].sudo(
            ).get_param('originate_prefix')
        strip_plus = self.env['asterisk_common.settings'].sudo(
            ).get_param('originate_strip_plus')
        # Iterate over contacts.
        for contact in contacts:
            # Check if the contact object has phone_normalized field.
            src_number = number = str(getattr(
                contact, 'phone_normalized', False) or contact.phone)
            if number:
                # Now transform the number according to outgoing dial rules.
                if originate_format != 'no_format' and getattr(
                        contact, '_format_number', False):
                    number = contact._format_number(
                        number, format_type=originate_format)
                # Strip formatting if present.
                number = number.replace(' ', '')
                number = number.replace('(', '')
                number = number.replace(')', '')
                number = number.replace('-', '')
                if number[0] == '+' and strip_plus:
                    # Remove + from the beginning.
                    number = number[1:]
                if originate_prefix:
                    number = '{}{}'.format(originate_prefix, number)
                try:
                    with mute_logger('odoo.sql_db'), self.env.cr.savepoint():
                        self.env['asterisk_dialer.contact'].create({
                            'phone': number,
                            'campaign': self.id,
                            'model_object': '{},{}'.format(
                                model, contact.id),
                        })
                        self.log(
                            'Import {} {} src number {} dst number {}'.format(
                                model, contact.name, src_number, number),
                            level='debug')
                except IntegrityError:
                    self.log('Phone {} already exists in campaign.'.format(
                        number))

    @api.model
    def manage_campaign(self):
        now = fields.Datetime.now()
        campaign_obj = self.env['asterisk_dialer.campaign']
        # Find scheduled campaigns
        campaigns_to_start = campaign_obj.search([
            ('start_type', '=', 'scheduled'),
            ('start_date', '<=', fields.Datetime.to_string(now)),
            ('state', 'in', ('paused', 'ready'))
        ])
        if campaigns_to_start:
            campaigns_to_start.write({
                'state': 'running',
            })
            for campaign in campaigns_to_start:
                campaign.wakeup()
        campaigns_to_stop = campaign_obj.search([
            ('end_date', '<=', fields.Datetime.to_string(now)),
            ('state', '!=', 'done')
        ])
        if campaigns_to_stop:
            campaigns_to_stop.write({
                'state': 'done'
            })
        # Find periodic campaigns in done state.
        periodic_campaigns = campaign_obj.search([
            ('start_type', '=', 'periodic'),
            ('state', '=', 'done'),
            ('next_run', '<=', datetime.now())])
        for per_camp in periodic_campaigns:
            per_camp.state = 'running'
            self.env['asterisk_dialer.contact'].search(
                [('campaign', '=', per_camp.id)]).unlink()
            # TODO: Re-run filter to re-generate contacts ???
            per_camp.generate_contacts(per_camp.model, per_camp.domain)
            per_camp.wakeup()

    def log(self, content, level='info'):
        self.ensure_one()
        # contact can be either message string or tupple(record, vals, fields).
        messages = []
        if type(content) is list:
            rec, vals, track_fields = content
            for field in track_fields:
                if vals.get(field):
                    # Get selection values
                    if isinstance(rec._fields[field], fields.Selection):
                        old_value = dict(rec._fields[field].selection).get(rec[field])
                        new_value = dict(rec._fields[field].selection).get(vals.get(field))
                    else:
                        old_value = rec[field]
                        new_value = vals.get(field)
                    if old_value != new_value:
                        messages.append('{} - {}: {} => {}'.format(
                            rec.name, field, old_value, new_value))
        else:
            messages.append(content)
        # Add log message to campaign
        if (self.log_level == 'i' and level[0] == 'i') or (
                self.log_level == 'd'):
            for msg in messages:
                self.env['asterisk_dialer.campaign_log'].create({
                    'campaign': self.id,
                    'content': msg,
                    'level': level[0],
                })
        # Log to console
        if level == 'info':
            logger.info('\n'.join(messages))
        if level == 'debug':
            logger.debug('\n'.join(messages))

    def msg_test(self):
        # Upload voice file to Asterisk and test it using Originate
        if self.msg_type == 'sound_file':
            if not self.msg_file:
                raise ValidationError('File not set!')
            # Copy file to Asterisk
            self.env.user.asterisk_agent.request(
                'asterisk.put_prompt',
                'dialer_campaign_{}.wav'.format(self.id),
                self.msg_file.decode('latin-1'))
        else:
            if not self.tts_text:
                raise ValidationError('Message text not set!')
            if not self.contacts:
                raise ValidationError('Please add a test contact!')
            self.render_voice_message(self.contacts[0])
        # Originate a call to playback it
        self.env['asterisk_dialer.channel'].originate(
            channel=self.env.user.asterisk_user.channels[0].channel,
            app='AGI',
            data='agi:async',
            campaign=self,
            contact=self.contacts[0],
        )

    def action_archive(self):
        # Archive campaigns logs and contacts when campaign is archived
        for rec in self:
            self.env['asterisk_dialer.campaign_log'].search([('campaign', '=', rec.id)]).toggle_active()
            self.env['asterisk_dialer.contact'].search([('campaign', '=', rec.id)]).toggle_active()
            rec.filtered(lambda record: record[rec._active_name]).toggle_active()

    def action_unarchive(self):
        # Unarchive campaigns logs and contacts when campaign is unarchived
        for rec in self:
            self.env['asterisk_dialer.campaign_log'].with_context(active_test=False).search([
                ('campaign', '=', rec.id)]).toggle_active()
            self.env['asterisk_dialer.contact'].with_context(active_test=False).search([
                ('campaign', '=', rec.id)]).toggle_active()
            rec.filtered(lambda record: not record[rec._active_name]).toggle_active()

    @api.onchange('tts_text')
    def reset_is_common_tts_created(self):
        self.is_common_tts_created = False
