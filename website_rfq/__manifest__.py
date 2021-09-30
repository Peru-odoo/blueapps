# -*- coding: utf-8 -*-
{
    "name": "Website Request for Quotation",
    "version": "0.1.0.1",
    "license": "OPL-1", 
    "author": "Vision to Motion Myanmar Co., Ltd.",
    "website": "https://www.v2m.io",
    "category": "eCommerce",    
    "summary": "To make request for quotation on ecommerce website, without displaying product price. This is good especially for Enterprise and B2B products sales ",
    "description": """
    Purpose :- 
    To make request for quotation on ecommerce website.
    """,    
    'depends': ['website','website_sale','sale_management','website_sale_comparison','website_sale_wishlist'],
    "price" : "0.0",
    "currency"  : "USD",
    "support" : "support@v2m.jp",
    "images": [],
    "data": [
        'security/ir.model.access.csv',        
        'views/product_view.xml',
        'views/templates.xml',
        'views/rfq_report.xml',
        'views/request_for_quotation_report.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
}
