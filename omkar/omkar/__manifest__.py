# -*- coding: utf-8 -*-
{
    'name': "omkar",

    'summary': """
        omkar_automobile""",

    'description': """
        omkar automobile
    """,

    'author': "Shivam Kachhia",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Garage',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'reports/reports.xml',
        # 'views/templates.xml',
    ],
    'license': 'AGPL-3',
    'images': ['static/description/icon.png'],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,

}
