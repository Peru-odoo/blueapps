# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
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

from odoo import api, fields, models, _

class PartnerStage(models.Model):
    _name = "partner.stage"
    _order = "sequence"
    _description = 'Partner Stage'

    name = fields.Char(string = 'Partner Stages', help = 'Enter Stages for Partners', required =True)
    customer = fields.Boolean(string = 'Visible to Customers?')
    vendor = fields.Boolean(string = 'Visible to Vendors?')
    sequence = fields.Integer(string = 'Sequence', help = 'Enter Sequence Number')






