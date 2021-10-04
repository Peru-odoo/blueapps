# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
# -*- encoding: utf-8 -*-
{
    'name': 'Asterisk Calls Helpdesk',
    'version': '1.0',
    'author': 'Odooist',
    'price': 100,
    'currency': 'EUR',
    'maintainer': 'Odooist',
    'support': 'odooist@gmail.com',
    'license': 'OPL-1',
    'category': 'Phone',
    'summary': 'Asterisk Calls Helpdesk integration',
    'description': "",
    'depends': ['helpdesk', 'asterisk_calls'],
    'data': [
        'security/agent.xml',
        'views/ticket.xml',
        'views/call.xml',
        'views/channel.xml',
        'views/resources.xml',
    ],
    'demo': [],
    "qweb": ['static/src/xml/*.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/history_graph_crm.png'],
}
