{
    'name': 'Integração com Whatsapp - Aguias',
    'version': '14.0.0.1',
    'summary': 'Whatsapp Odoo Connector',
    'author': 'Diego Santos, Saaragh Technologies Pte Ltd',
    'company': 'BlueConnect',
    'maintainer': 'BlueConnect',
    'images': ['static/description/Banner.png'],
    'sequence': 4,
    'license': 'OPL-1',
    'description': """Whatsapp Odoo Connector""",
    'category': 'Connector',
    'depends': [
        'base', 'contacts', 'sale', 'crm', 'sale_management', 'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'models/whatsapp_template.xml',
        'views/whatsapp_button_views.xml',
        'wizard/whatsapp_wizard.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
