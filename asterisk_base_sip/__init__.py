import random
import string
from .import models
from .import wizards
from odoo.addons.asterisk_base.utils import generate_password
from odoo.addons.asterisk_common.models.agent import AgentError


def do_post_install(cr, registry):
    # Here we replace manually created SIP peers with base sip peers.
    from odoo import api, SUPERUSER_ID
    import logging
    logger = logging.getLogger(__name__)    
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Create SIP peers for existing users.
        users = env['asterisk_common.user'].search([])
        for user in users:
            # Create a Route Group for users
            route_group = env.ref('asterisk_base_sip.default_route_group')
            user.route_groups = [(4, route_group.id)]
            user_channels = [
                k.channel for k in user.channels if 'SIP' in k.channel.upper()]
            for ch in user_channels:
                logger.info('Creating SIP channel %s.', ch)
                ch_type, ch_name = ch.split('/')
                env['asterisk_base_sip.peer'].create({
                    'server': user.server.id,
                    'template': env.ref(
                        'asterisk_base_sip.natuser_peer_template').id,
                    'secret': generate_password(),
                    'user': user.id,
                    'name': ch_name,
                    'host': 'dynamic',
                    'peer_type': 'user',
                    'channel_type': ch_type.lower()})
            # Create extensions
            env['asterisk_base.extension'].create_extension_for_obj(user)
        """
        # TODO: THIS DOES NOT WORK DUE TO ODOO BUG.        
        # Notify Agent to reload events.
        logger.info('Reload Asterisk Agent events.')
        for agent in env['remote_agent.agent'].search([]):
            logger.info(
                'Sending reload events command to %s', agent.system_name)
            try:
                agent.action({'Action': 'ReloadEvents'},
                         notify=True, no_wait=True, delay=30)
            except AgentError:
                pass
        """
    return True


def do_uninstall(cr, registry):
    from odoo import api, SUPERUSER_ID
    import logging
    """
    # TODO: THIS DOES NOT WORK DUE TO ODOO BUG.    
    logger = logging.getLogger(__name__)
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Notify Agent to reload events.
        logger.info('Reload Asterisk Agent events.')
        for agent in env['remote_agent.agent'].search([]):
            logger.info(
                'Sending reload events command to %s', agent.system_name)
            try:
                agent.action({'Action': 'ReloadEvents'},
                         notify=True, no_wait=True, delay=30)
            except AgentError:
                pass       
    return True
    """