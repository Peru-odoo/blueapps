# Copyright 2021 BlueConnect
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Transferencia(models.TransientModel):

    _name = 'transferencia'

    name = fields.Char()

    @api.multi
    def doit(self):
        for wizard in self:
            # TODO
            pass
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Action Name',  # TODO
            'res_model': 'result.model',  # TODO
            'domain': [('id', '=', result_ids)],  # TODO
            'view_mode': 'form,tree',
        }
        return action
