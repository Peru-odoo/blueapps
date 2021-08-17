# -*- coding: utf-8 -*-
#######################################################

#   CorpoEureka - Innovation First!
#
#   Copyright (C) 2021-TODAY CorpoEureka (<https://www.corpoeureka.com>)
#   Author: CorpoEureka (<https://www.corpoeureka.com>)
#
#   This software and associated files (the "Software") may only be used (executed,
#   modified, executed after modifications) if you have pdurchased a vali license
#   from the authors, typically via Odoo Apps, or if you have received a written
#   agreement from the authors of the Software (see the COPYRIGHT file).
#
#   You may develop Odoo modules that use the Software as a library (typically
#   by depending on it, importing it and using its resources), but without copying
#   any source code or material from the Software. You may distribute those
#   modules under the license of your choice, provided that this license is
#   compatible with the terms of the Odoo Proprietary License (For example:
#   LGPL, MIT, or proprietary licenses similar to this one).
#
#   It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#   or modified copies of the Software.
#
#   The above copyright notice and this permission notice must be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

# 	Responsable CorpoEureka: Jose Mazzei
##########################################################################

{
    'name': 'Total Cost on Sale Order',
    'description': 'This module adds the Total Cost on sales order this gives the profitability by calculating the difference between the Amount Total and Cost Price.',
    'summary': 'This gives the profitability by calculating the difference between the amount total and cost price.',
    'version':'14.0.1',
    'category': 'Sale',
    'author': 'CorpoEureka',
    'company': 'CorpoEureka',
    'maintainer': 'CorpoEureka',
    'support': 'soporte_odoo@corporacioneureka.com',
    'website' : 'https://www.corpoeureka.com',
    'license': 'AGPL-3',
    'depends':[
        'sale_management',
        'sale_margin'
    ],
    'data':[
        'views/sale_margin_view.xml'
    ],
    'price': 0.00,
    'currency': 'USD',
    'images': ['static/description/eu_screenshot.png'],
    'installable': True,
    'application': True,
    'demo': '',
}
