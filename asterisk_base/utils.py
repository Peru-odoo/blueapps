# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
# -*- coding: utf-8 -*-
import logging
import random
import unicodedata
import re
import string
from odoo.exceptions import Warning, ValidationError, UserError
from odoo.tools import ustr
from odoo.http import request
from odoo import release

logger = logging.getLogger(__name__)

RANDOM_PASSWORD_LENGTH = 8
CONF_LINE = re.compile(r'^[^\S^t]+(.+)$')


def generate_password(length=RANDOM_PASSWORD_LENGTH):
    chars = string.ascii_letters + string.digits
    password = ''
    while True:
        password = ''.join(map(lambda x: random.choice(chars), range(length)))
        if filter(lambda c: c.isdigit(), password) and \
                filter(lambda c: c.isalpha(), password):
            break
    return password


def slugify(s, max_length=None):
    s = ustr(s)
    uni = unicodedata.normalize('NFKD', s).encode(
                                            'ascii', 'ignore').decode('ascii')
    slug_str = re.sub('[\W_]', ' ', uni).strip().lower()
    slug_str = re.sub('[-\s]+', '-', slug_str)
    return slug_str[:max_length]


def is_debug_mode_enabled():
    try:
        debug = request.session.debug if release.version_info[0] >= 13 \
            else request.debug
        return debug
    except RuntimeError:
        pass


def get_default_server(element):
    try:
        return element.env.ref('asterisk_base.default_server').id
    except Exception:
        # On init there is noone
        return False
