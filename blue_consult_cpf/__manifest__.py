{  # pylint: disable=C8101,C8103
    'name': 'BlueConnect - Consultar CPF',
    'description': 'Modifies address forms',
    'version': '14.0.1.0.0',
    'category': 'Localization',
    'author': 'BlueConnect',
    'license': 'OEEL-1',
    'website': 'https://www.blueconnect.com,br',
    'contributors': [
        'Diego Santos <diego.blueconnect@gmail.com>',
    ],
    'depends': [
        'blue_consignado',
        'crm',
    ],
    'data': [
#        'data/configuration.xml',
#        'data/res.country.csv',
#        'data/res.country.state.csv',
        'views/res_partner.xml',
#        'views/res_city.xml',
#        'views/res_company.xml',
    ],
}
