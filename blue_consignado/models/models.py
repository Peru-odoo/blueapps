# -*- coding: utf-8 -*-
from odoo import models, fields, api


 class blue_consultar_cpf(models.Model):
     _name = 'blue_consultar_cpf.blue_consultar_cpf'
     _description = 'blue_consultar_cpf.blue_consultar_cpf'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
