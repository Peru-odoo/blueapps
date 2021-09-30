# See LICENSE file for full copyright and licensing details.

{
    'name': 'Whatsapp Sale',
    'version': '14.0.0.1.0',
    'license': 'OPL-1',
    'author': "Alphasoft",
    'sequence': 1,
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'summary': 'This module is used for Whatsapp Sale',
    'category': 'Extra Tools',
    'depends': ['base_automation', 'sale', 'aos_whatsapp'],
    'data': [
        'data/sale_data.xml',
        'views/sale_order.xml',
        'wizard/whatsapp_compose_view.xml',
    ],
    'external_dependencies': {'python': ['html2text']},
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    'price': 0,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}
