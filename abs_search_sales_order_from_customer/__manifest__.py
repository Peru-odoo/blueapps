# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
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
#################################################################################
{
    'name'        :"Search Sales Order From Customer",
    'author'      :'Ascetic Business Solution',
    'category'    :'Sales',
    'summary'     :"""Search Sales Order From Customer""",
    'website'     :'http://www.asceticbs.com',
    'description' :""" Search Sales Order From Customer """,
    'version'      :'14.0.1.0',
    'depends'     :['sale_management'],
    'data'        :[
                    'security/ir.model.access.csv',
                    'wizard/customer_wizard_view.xml',
                    'views/customer_list_view.xml',
                    'views/configuration_search_view.xml'
                   ],
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'installable' :True,
    'application' :True,
    'auto_install':False,
}
