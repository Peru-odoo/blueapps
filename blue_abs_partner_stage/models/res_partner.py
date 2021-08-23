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

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _default_stage_id(self):
        result = super(ResPartner, self).default_get('customer')
        stages_final = False
        stages = []
        if self.env.context.get('search_default_customer',False) == 1:
            stages = self.env['partner.stage'].search([('customer','=',True)])
        elif self.env.context.get('search_default_supplier',False) == 1:
            stages = self.env['partner.stage'].search([('vendor','=',True)])
        stage_list = []
        stage_return = False
        for stage in stages:
            stage_list.append(stage.sequence)
        if stage_list:
            stage_return = min(stage_list)
        if stage_return:
            stages_final = self.env['partner.stage'].search([('sequence','=',stage_return)])[0]
        if stages_final:
            return stages_final.id
        else:
            return False

    stage_id = fields.Many2one('partner.stage', string='Stages', default=lambda self: self._default_stage_id(), track_visibility='onchange', copy=False)
