from odoo import models, fields, Command
from odoo.exceptions import ValidationError


class MergeSaleOrderWizard(models.TransientModel):
    _name = 'merge.sale.order.wizard'
    _description = 'Merge Sale Order Wizard'

    merge_options = fields.Selection(string='Merger Option', selection=[('merge_create_cancel', 'Merge Create Cancel'),
                                                                        ('merge_create_delete', 'Merge Create Delete'),
                                                                        ('merge_existing_cancel',
                                                                         'Merge Existing Cancel'),
                                                                        ('merge_existing_delete',
                                                                         'Merge Existing Delete')],
                                     help='merger option of the sale oder wizard')
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order Id',
                                    help='Sale order id of the merge sale order wizard')

    def create_order(self):
        selected_orders = self.env['sale.order'].browse(self.env.context.get('active_ids'))
        new_order_lines = []
        partner = selected_orders[0].partner_id
        products = []
        for orderline in selected_orders.order_line:
            if orderline.order_id.partner_id.id != partner.id and orderline.order_id.state != 'draft':
                raise ValidationError(
                    'Warning !!!!  Selected Sale Order belong to different Customer it cannot be merged')
            else:
                if orderline.product_id.id in products:
                    orderlines = list(filter(
                        lambda line: line[2]['product_id'] == orderline.product_id.id and
                                     line[2]['price_unit'] == orderline.price_unit and
                                     line[2]['tax_id'] == orderline.tax_id, new_order_lines))

                    orderlines_products = list(filter(lambda line: (
                                line[2]['product_id'] == orderline.product_id.id and (
                                    line[2]['price_unit'] != orderline.price_unit or line[2][
                                'tax_id'] != orderline.tax_id)), new_order_lines))
                    if orderlines:
                        orderlines[0][2]['product_uom_qty'] += orderline.product_uom_qty
                    elif orderlines_products:
                        new_order_lines.append(Command.create({'product_id': orderline.product_id.id,
                                                               'product_uom_qty': orderline.product_uom_qty,
                                                               'price_unit': orderline.price_unit,
                                                               'tax_id': orderline.tax_id
                                                               }))
                else:
                    products.append(orderline.product_id.id)
                    new_order_lines.append(Command.create({'product_id': orderline.product_id.id,
                                                           'product_uom_qty': orderline.product_uom_qty,
                                                           'price_unit': orderline.price_unit,
                                                           'tax_id': orderline.tax_id
                                                           }))
        if self.merge_options in ['merge_create_cancel', 'merge_create_delete']:
            vals = {'partner_id': partner.id, 'order_line': new_order_lines}
            self.env['sale.order'].create(vals)
            for order in selected_orders:
                if self.merge_options == 'merge_create_cancel':
                    order.state = 'cancel'
                else:
                    order.unlink()
        elif self.merge_options in ['merge_existing_cancel', 'merge_existing_delete']:
            [orderline.unlink() for orderline in self.sale_order_id.order_line]
            self.sale_order_id.write({'order_line': new_order_lines})
            for order in selected_orders.filtered(lambda order: order not in self.sale_order_id):
                if self.merge_options == 'merge_existing_cancel':
                    order.state = 'cancel'
                else:
                    order.unlink()
