from odoo import models, fields, api, Command


class ProductStockUpdateEpt(models.TransientModel):
    _name = 'product.stock.update.wizard.ept'
    _description = 'Product Stock Update Ept'

    location_id = fields.Many2one(comodel_name='stock.location.ept', string='Location',
                                  help='Location of the product stock')
    available_stock = fields.Float(string='System Quantity', help='System Quantity of the Product Stock.')
    counted_qty = fields.Float(string='Counted Quantity', help='Counted Quantity of the Product Stock.')
    difference_qty = fields.Float(string='Inventory Adjustment',
                                  help='Difference Inventory Adjustment of the product stock.',
                                  compute='_compute_difference', store=False)

    def _compute_difference(self):
        for product in self:
            product.difference_qty = self.available_stock - self.counted_qty

    @api.onchange('location_id')
    def onchange_location(self):
        if self.location_id:
            product = self.env['product.ept'].browse(self.env.context.get('active_id'))
            self.available_stock = product.with_context(location=self.location_id).product_stock

    def update_stock(self):
        product = self.env['product.ept'].browse(self.env.context.get('active_id'))
        inventory_lines = []
        inventory_lines.append(Command.create({'product_id': self.env.context.get('active_id'),
                                               'available_qty': self.available_stock,
                                               'counted_product_qty': self.counted_qty,
                                               'difference': self.difference_qty}))

        invenotry = self.env['stock.inventory.ept'].create({'name': product.name + '  ' + 'Inventory Adjustment',
                                                            'location_id': self.location_id.id,
                                                            'inventory_line_ids': inventory_lines})
        invenotry.validate_inventory()
