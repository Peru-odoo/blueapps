# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError
from odoo.addons.asterisk_common.models.user import USER_PERMITTED_FIELDS

logger = logging.getLogger(__name__)

USER_PERMITTED_FIELDS.extend([
    'call_waiting', 'vm_enabled', 'ring_channels',
    'vm_on_unavail_enabled', 'vm_on_busy_enabled',
    'vm_email', 'cf_on_busy_enabled',
    'vm_max_length', 'cf_uncond_enabled',
    'cf_on_busy_number', 'cf_on_unavail_enabled',
    'vm_max_messages', 'cf_on_unavail_number',
    'vm_direct_call_enabled', 'cf_uncond_number',
])


class BaseSipUserChannel(models.Model):
    _inherit = 'asterisk_common.user_channel'
    _order = 'sequence'

    channel = fields.Char(required=False) # Override required attr.
    comp_channel = fields.Char(
        required=True, compute='_get_channel', inverse='_set_channel',
        string='Channel')
    sip_peer = fields.Many2one('asterisk_base_sip.peer')
    ring_enabled = fields.Boolean(default=True, string='Ring')
    ring_timeout = fields.Integer(default=30)

    @api.model
    def create(self, vals):
        channel = super(BaseSipUserChannel, self).create(vals)
        # Search for existing SIP peer 
        # 1. Check that SIP peer does not belong to other user.
        # 2. Check that this channel is not already defined for other user.
        # TODO: Create a SIP peer from here.
        channel.create_sip_peer()
        return channel

    def create_sip_peer(self):
        self.ensure_one()
        # Check that there is not yet a SIP peer for this user
        sip_peer = self.env['asterisk_base_sip.peer'].search([
            ('user', '=', self.asterisk_user.id)])
        if not sip_peer and self.channel.startswith('SIP'):
            sip_peer.with_context(
                no_create_channel=True).create({
                'name': self.asterisk_user.exten,
                'user': self.asterisk_user.id,
                'host': 'dynamic',
                'peer_type': 'user',
            })
        if not self.env.context.get('no_build_conf'):
            self.env['asterisk_common.user'].build_conf()

    def _get_channel(self):
        for rec in self:
            if rec.sip_peer:
                # Get channel from SIP peer.
                rec.comp_channel = '{}/{}'.format(
                    rec.sip_peer.channel_type.upper(), rec.sip_peer.name)
            else:
                # Get channel from original channel field
                rec.comp_channel = rec.channel

    def _set_channel(self):
        for rec in self:
            rec.channel = rec.comp_channel
            # Set SIP name for related SIP peers.
            if rec.sip_peer:
                rec.sip_peer.name = rec.comp_channel.split('/')[1]

    @api.constrains('comp_channel')
    def _check_peers(self):
        for rec in self:
            chan, name = rec.comp_channel.split('/')
            if not rec.sip_peer and self.env['asterisk_base_sip.peer'].search(
                    [('agent', '=', rec.agent.id),
                     ('name', '=', name),
                     ('channel_type', '=', chan.lower())]):
                raise ValidationError(
                    _('Channel {} is already defined in SIP -> Peers!').format(
                        rec.comp_channel))

    def _get_originate_context(self):
        for rec in self:
            if rec.sip_peer:
                rec.originate_context = rec.sip_peer.context
            else:
                rec.originate_context = rec.context

    def unlink(self):
        for rec in self:
            if rec.sip_peer and rec.sip_peer.user:
                if not self.env.context.get('from_peer'):
                    rec.sip_peer.user = False
        return super(BaseSipUserChannel, self).unlink()

    def _set_originate_context(self):
        for rec in self:
            if rec.sip_peer:
                rec.sip_peer.context = rec.originate_context
            else:
                rec.context = rec.originate_context

    def open_peer_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'asterisk_base_sip.peer',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'res_id': self.sip_peer.id,
            'view_id': self.env.ref(
                'asterisk_base_sip.asterisk_base_sip_peer_user_form').id,
        }


class BaseSipUser(models.Model):
    _inherit = 'asterisk_common.user'

    accountcode = fields.Char(compute='_get_accountcode')
    route_groups = fields.Many2many(
        'asterisk_base_sip.route_group',
        required=True, string='SIP Route Groups',
        relation='asterisk_base_sip_user_route_groups')
    callerid_numbers = fields.One2many(
        'asterisk_base_sip.translation', string='CallerID Translations',
        inverse_name='src_user', readonly=True)
    dialplan = fields.Text(compute='_get_dialplan')
    ring_channels = fields.One2many(
        'asterisk_common.user_channel', string='Channels',
        inverse_name='asterisk_user')
    call_waiting = fields.Boolean()
    # VoiceMail
    vm_enabled = fields.Boolean(string="VoiceMail")
    vm_on_busy_enabled = fields.Boolean(string="On Busy")
    vm_on_unavail_enabled = fields.Boolean(string='On Unavailable')
    vm_email = fields.Char(string='E-Mail Address')
    vm_direct_call_enabled = fields.Boolean(string='Direct Mailbox Call')
    vm_max_length = fields.Integer(default=120, string='Max Message Duration')
    vm_max_messages = fields.Integer(default=30, string='Max Messages / Inbox')
    # Call forward
    cf_on_busy_enabled = fields.Boolean('On Busy')
    cf_on_busy_number = fields.Char(string='On Busy Number')
    cf_on_unavail_enabled = fields.Boolean('On Unavailable')
    cf_on_unavail_number = fields.Char(string='On Unavailable Number')
    cf_uncond_enabled = fields.Boolean('Unconditional')
    cf_uncond_number = fields.Char(string='Unconditional Number')

    def _get_dialplan(self):
        for rec in self:
            data = self.env['asterisk_base.conf_template'].render_template(
                'user_in_dialplan', rec.server.id, {'rec': rec})
            rec.dialplan = data

    def build_extension(self):
        self.ensure_one()
        return self.env['asterisk_base.conf_template'].render_template(
            'user_extension', self.server.id, {'rec': self})

    @api.model
    def build_conf(self):
        users = self.env['asterisk_common.user'].search([])
        for server in users.mapped('server'):
            conf_data = ''
            for u in users.filtered(lambda r: r.server == server):
                conf_data += u.dialplan
                conf_data += '\n\n'
            conf = self.env['asterisk_base.conf'].get_or_create(
                server.id, 'extensions_odoo_user.conf')
            conf.content = conf_data
            conf.include_from('extensions.conf')

    def _get_extension_name(self):
        for rec in self:
            rec.extension_name = rec.user.name

    @api.onchange('agent', 'server')
    def _reset_route_groups(self):
        if not self.server:
            self.route_groups = False
        else:
            if not self.route_groups or self._origin.server != self.server:
                groups = self.env['asterisk_base_sip.route_group'].search(
                    [('server', '=', self.server.id),
                     ('is_user_default', '=', True)])
                self.route_groups = groups
            return {'domain': {
                'route_groups': [('server', '=', self.server.id)]}}

    @api.onchange('user', 'cf_on_busy_enabled', 'cf_on_unavail_enabled',
                  'cf_uncond_enabled')
    def _change_vm_and_cf(self):
        try:
            if not self.user:
                return
            # VoiceMail
            if not self.vm_email or \
                    self._origin.vm_email == \
                    self._origin.user.partner_id.email:
                self.vm_email = self.user.partner_id.email
            # Get user's number
            old_number = self._origin.user.partner_id.mobile_normalized or \
                self._origin.user.partner_id.phone_normalized
            new_number = self.user.partner_id.mobile_normalized or \
                self.user.partner_id.phone_normalized
            # CF on Unconditional
            if not self.cf_on_busy_number or \
                    self._origin.cf_on_busy_number == old_number:
                self.cf_on_busy_number = new_number
            # CF on Unavailable
            if not self.cf_on_unavail_number or \
                    self._origin.cf_on_unavail_number == old_number:
                self.cf_on_unavail_number = new_number
            # CF Unconditional
            if not self.cf_uncond_number or \
                    self._origin.cf_uncond_number == old_number:
                self.cf_uncond_number = new_number
        except Exception:
            logger.exception('Change VM & CF error:')

    @api.constrains('vm_enabled', 'vm_on_busy_enabled', 'vm_on_unavail_enabled')
    def _require_b_or_u(self):
        for rec in self:
            if rec.vm_enabled and not (
                    rec.vm_on_busy_enabled or rec.vm_on_unavail_enabled):
                raise ValidationError(
                    "Please select when to enable the voicemail.")

    @api.onchange('vm_enabled')
    def _set_b_and_u(self):
        if self.vm_enabled:
            self.vm_on_unavail_enabled = True
            self.vm_on_busy_enabled = True
        else:
            self.vm_on_unavail_enabled = False
            self.vm_on_busy_enabled = False

    def get_ring_channels_dial_string(self):
        # Called from conf templates to get  dial string for all channels.
        self.ensure_one()
        if self.ring_channels:
            return '&'.join(
                [k.channel for k in self.ring_channels if k.ring_enabled])
        else:
            return ''

    def _get_accountcode(self):
        for rec in self:
            rec.accountcode = 'user-{}'.format(rec.id)

    def get_ring_channels_timeout(self):
        # Called from conf templates to get max timeout of all channels
        self.ensure_one()
        return max([k.ring_timeout for k in self.ring_channels] or [60])
