from .import models
from .import controllers


def do_post_install(cr, registry):
    # Here we replace manually created SIP peers with base sip peers.
    from odoo import api, SUPERUSER_ID
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        users = env['asterisk_common.user'].search([])
        # Set server value for users
        for user in users:
            server = env['asterisk_base.server'].search(
                [('agent', '=', user.agent.id)])
            user.server = server
