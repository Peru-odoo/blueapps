# -*- coding: utf-8 -*-
{
    'name': 'Customer Search Filter',
    'author': 'Aktiv Software',
    'category': 'Sales',
    'license': 'AGPL-3',
    'website': 'www.aktivsoftware.com',
    'version': '14.0.1.0.1',
    'summary': '''
                This module helps in finding a customer with respect to its
                mobile number, phone number, city,
                email and its job position.
            ''',
    'description': '''
                    The Module - Customer Search Filter is purposefully
                    developed to ease the end user in finding a customer as
                    per its mobile & phone number, city,
                    email and its job position. This functionality
                    is used when we want to search customer in any object.
                ''',
    'depends': ['base'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
