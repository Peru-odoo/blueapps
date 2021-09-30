# Copyright 2020 Openindustry.it SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Import file from PON CAD a 3D Scaffolding Design Software BIM",
    "version": "14.0.2.0.0",
    "license": "AGPL-3",
    "summary": "Import file from PON CAD a 3D Scaffolding Design Software BIMImport Poncad",
    "category": "Tools",
    "description": """Import file from PON CAD a 3D Scaffolding Design Software BIM
developed to help Designers, Renters and Producers of small and big structures.
    """,
    "company": "https://openindustry.it",
    "author": "andrea.m.piovesana@gmail.com, mf2965@gmail.com",
    "website": "https://www.meccad.net/software-cad-3d-scaffolding/",
    "depends": [
        "sale_management",
        "sale_stock",
        "purchase",
    ],
    "data": [
        "wizards/product.xml",
        "security/ir.model.access.csv",
    ],
    "images": [
        "images/import_poncad.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "price": 0,
    "currency": "EUR",
}
