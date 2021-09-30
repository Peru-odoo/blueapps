# Copyright 2020 Openindustry.it SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, exceptions, api, _
from odoo.exceptions import Warning, UserError
import logging
import csv
import base64
import io

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProductImportWizard(models.TransientModel):
    _name = "product.template.import.wizard"

    partner_id = fields.Many2one('res.partner', required=True)
    file = fields.Binary('File')
    multi = fields.Boolean('Multi Phase')
    origin = fields.Char('Origin')
    log = []

    def import_csv(self):
        try:
            file_to_import = base64.b64decode(self.file)
            data_file = io.StringIO(file_to_import.decode("utf-8"))
            data_file.seek(0)
            reader = csv.reader(data_file, delimiter=';')
            lines = []
            # cad file
            self.origin = ' '
            for index, row in enumerate(reader):
                self.origin = row[0]
                break
            #lines
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                if row[1] == '':
                    continue
                if row[3] == '':
                    continue
                values = {
                    'PHASE': str(row[0]),
                    'CODE': str(row[1]),
                    'NAME': str(row[2]),
                    'QTY': str(row[3]),
                    'PRICE': str(row[4]),
                    'WEIGHT': str(row[5]),
                }
                lines.append(values)
                logging.info("Read product " + row[1])
        except Exception as e:
            raise UserError(e)
        # create product if not exist
        self._load_products(lines)
        # create sale order
        self._create_sale_order(lines)

    def _load_products(self, lines):
        product = self.env['product.template']
        route = self.env['stock.location.route']
        #route_mto = route.search([('name', 'like', _('Make To Order'))], limit=1).id
        #route_man = route.search([('name', 'like', _('Manufacture'))], limit=1).id
        route_buy = route.search([('name', 'like', _('Buy'))], limit=1).id
        for index, row in enumerate(lines):
            product_code = row['CODE']
            product_name = row['NAME']
            product_list_price = row['PRICE']
            product_weight = row['WEIGHT']
            product_obj = product.search([('default_code', '=', product_code)], limit=1)
            #logging.info("Read product " + product_code)
            if not product_obj:
                product_vals = {
                    'default_code': product_code,
                    'name': product_name,
                    'type': 'product',
                    'list_price': product_list_price,
                    'weight': product_weight,
                    'invoice_policy': 'delivery',
                    'route_ids': [(6, 0, [route_buy])],
               }
                product_obj = product.with_context(tracking_disable=True).create(product_vals)
                if product_obj:
                    logging.info("Created product " + product_code)
            else:
                logging.info("Product already exist " + product_code)
        self.env.cr.commit()
        return

    def _create_sale_order(self, lines):

        product = self.env['product.product']
        phase_prec = ' '
        for index, row in enumerate(lines):
            phase = row['PHASE']
            product_code = row['CODE']
            product_name = row['NAME']
            product_obj = product.search([('default_code', '=', product_code)], limit=1)
            qty = int(row['QTY'])
            if phase_prec != phase and phase_prec != '***':
                order_vals = {
                    'partner_id': self.partner_id.id,
                    'client_order_ref': phase,
                    'origin': self.origin,
                }
                sale_order = self.env['sale.order'].create(order_vals)
                n = 0
            if self.multi:
                phase_prec = phase
            else:
                phase_prec = '***'
            n += 1
            orderline_vals = {
                'order_id': sale_order.id,
                'sequence': n,
                'product_id': product_obj.id,
                'name': product_name,
                'product_uom': product_obj.uom_id.id,
                'product_uom_qty': qty,
            }
            sale_order_line = self.env['sale.order.line'].create(orderline_vals)

        return True
