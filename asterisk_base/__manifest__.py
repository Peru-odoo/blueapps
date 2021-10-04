# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
{
    'name': 'Asterisk Base',
    'summary': 'VoIP network management',
    'description': """Run your Asterisk server(s) from Odoo.""",
    'version': '1.10',
    'category': 'Phone',
    'author': 'Odooist',
    'license': 'OPL-1',
    'price': '200',
    'currency': 'EUR',
    'depends': ['web', 'mail', 'asterisk_common'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'do_post_install',
    'data': [
        # Security rules
        'security/agent/agent_record_rules.xml',
        'security/agent/agent_model_access.xml',
        'security/admin/admin_model_access.xml',
        'security/admin/admin_record_rules.xml',
        # Data
        'data/server.xml',
        'data/security_list.xml',
        'data/base_conf_templates.xml',
        'data/base_events.xml',
        'data/dialplans.xml',
        # Views
        'views/settings.xml',
        'views/assets.xml',
        'views/conf.xml',
        'views/conf_template.xml',
        'views/extension.xml',
        'views/dialplan.xml',
        'views/ir_cron.xml',
        'views/res_partner.xml',
        'views/server.xml',
        'views/security.xml',
        # Demo
        'demo/dialplan.xml',
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'images': ['static/description/odoo_asterisk.png'],
}
