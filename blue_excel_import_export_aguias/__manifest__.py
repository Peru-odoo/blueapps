# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Excel Importar/Exportar/Relatorios Aguias",
    "version": "14.0.1.0.2",
    "author": "Diego Santos, Ecosoft,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/server-tools",
    "category": "Tools",
    "depends": ["excel_import_export", "sale_management", "crm"],
    "data": [
        "import_export_sale_order/actions.xml",
        "import_export_sale_order/templates.xml",
#        "import_export_purchase_order/actions.xml",
#        "import_export_purchase_order/templates.xml",
        "report_sale_order/report_sale_order.xml",
        "report_sale_order/templates.xml",
        "report_sale_order/security/ir.model.access.csv",
        "report_crm_lead/report_crm_lead.xml",
        "report_crm_lead/templates.xml",
        "report_crm_lead/security/ir.model.access.csv",
        "import_sale_orders/menu_action.xml",
        "import_sale_orders/templates.xml",
        # Use report action
        "report_action/sale_order/report.xml",
        "report_action/sale_order/templates.xml",
        "report_action/crm_lead/report.xml",
        "report_action/crm_lead/templates.xml",
#        "report_action/partner_list/report.xml",
#        "report_action/partner_list/templates.xml",
#        "report_action/partner_list/report_partner_list.xml",
#        "report_action/partner_list/security/ir.model.access.csv",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["kittiu"],
}
