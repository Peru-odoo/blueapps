# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
import logging
from odoo import api, SUPERUSER_ID

logger = logging.getLogger(__name__)


def migrate(cr, version):
    logger.info('ODOOPBX: MIGRATING DIALPLAN...')
    try:
        cr.execute("""
            UPDATE asterisk_base_dialplan SET custom_dialplan = 
                REPLACE(custom_dialplan, 'object.', 'rec.')
        """)
        cr.commit()
        logger.info('ASTERISK BASE 1.8 DIALPLAN UPDATED.')
    except Exception as e:
        logger.exception('ASTERISK BASE 1.8 MIGRATE ERROR: %s', e)


