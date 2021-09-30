from odoo import api, models, fields


class ContactRefFour(models.Model):
    _inherit = 'res.partner'
    x_refe_fourn=fields.Char(string='Reference')

    @api.model
    def create(self, vals):
        for val in list(vals):
            if 'supplier_rank' in val:
                vals['x_refe_fourn'] = self.env['ir.sequence'].next_by_code('ref.four')
            elif 'customer_rank' in val:
                vals['x_refe_fourn'] = self.env['ir.sequence'].next_by_code('ref.cli')
        result = super(ContactRefFour, self).create(vals)
        return result


    @api.depends('name', 'x_refe_fourn')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.x_refe_fourn:
                name = '[' + po.x_refe_fourn + '] '+name
            result.append((po.id, name))
        return result