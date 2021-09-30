# -*- encoding: utf-8 -*-
{
	"name": "Gerar Oportunidade apartir do Cliente",
	"version": "14.0.1.2",
	"author": "Diego Santos",
	"website": "https://www.blueconnect.com.br",
	"sequence": 5,
	"depends": [
		"base",'sale_crm','sale','product'
	],
	"category": "Settings",
	"complexity": "easy",
	"description": """
	This module allow to add products on opportunity and create quote with that. 
	""",
	"data": [
		'security/ir.model.access.csv',
		'views/opportunity_product.xml',
		'views/res_partner.xml',		
		'views/contract_benefit.xml',	
	],
	"demo": [
	],
	"test": [
	],
	"auto_install": False,
	"installable": True,
	"application": False,
    'images': ['static/description/banner.png'],
	'license': 'LGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
