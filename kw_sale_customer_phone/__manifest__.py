{
    'name': 'Adds phone number to SO list',

    'summary': 'Phone number Odoo Sale module',

    'author': 'Kitworks Systems',
    'website': 'https://kitworks.systems/',

    'category': 'Other Category',
    'license': 'OPL-1',
    'version': '14.0.0.0.1',
    'depends': ['sale'
                ],
    'data': [
        'views/customer_phone_views.xml',
    ],
    'installable': True,

    'images': [
        'static/description/icon.png',
    ],
}
