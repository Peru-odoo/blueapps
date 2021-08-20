# -*- coding: utf-8 -*-
{
    'name': "inbox_notif_email",

    'summary': """
        odoo notification and email notification both""",

    'description': """
        It will add one more option to send notification via email and odoo notification both
    """,

    'author': "odoozone",
    'website': 'http://odoozone.com/',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Discuss',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail'],
    'license': 'LGPL-3',

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',],
        'images': [
'static/description/banner.PNG',
'static/description/icon.png',
'static/description/image1.png',
    ],
}
