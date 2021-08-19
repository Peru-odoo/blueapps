# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019  Erlangga Indra Permana  (https://erlaangga.github.io)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Odoo HTTP Json',
    'version': '1.0',
    'category': 'Web',
    'summary': 'Patch Odoo to support raw JSON response',
    'description': '''When we have some endpoints to use just like REST API in Odoo, we have response based on JsonRPC format.
This module allows you to bypass the required schema, so you can just call the endpoint with your JSON response.

You need to define this module in server wide modules configuration to activate since first running.''',
    'author': 'Erlangga Indra Permana',
    'website': 'https://erlaangga.github.io',
    'license': 'LGPL-3',
    'depends': [
        'web'
    ],
    'data': [
    ],
    'qweb': [
    ],
    'images':[],
    'application': False,
    'Category': 'Hidden',
    'auto_install': True,
}