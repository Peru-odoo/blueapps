# -*- coding: utf-8 -*-
{
    'name': "web_phone",
    'description': """Make calls using a VOIP system""",
    'currency': 'EUR',
    'price': '0',
    'version': '1.0',
    'category': 'Website/Website',
    'author': 'Odooist',
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False,
    'depends': ['website'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/user.xml',
    ],
    'demo': [],
    'js': ['static/src/lib/*.js',
           'static/src/js/*.js'],
    'qweb': [
        'static/src/xml/*.xml',
    ],
}
