# -*- coding: utf-8 -*-

{
    'name': 'PMS: Button in Kanban To Open Project',
    'version': '1.0.0.1',
    'summary': """Button in Project Kanban to open the project details.""",
    'description': """Button in Project Kanban to open the project details.""",
    'category': 'Services/Project',
    'author': 'iKreative',
    'website': "",
    'license': 'AGPL-3',

    'price': 0.0,
    'currency': 'USD',

    'depends': ['project'],

    'data': [
        'views/project_project_view.xml',

    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
