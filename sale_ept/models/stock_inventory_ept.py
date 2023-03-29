from odoo import models, fields


class StockInventoryEpt(models.Model):
    _name = 'stock.inventory.ept'
    _description = 'Stock Inventory Ept'

    name = fields.Char(string='Inventory Name', help='Name of the inventory')
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'), ('in-progress', 'In-Progress'), ('done', 'Done'),
                                        ('cancelled', 'Cancelled')], help='State of the Inventory.',default='draft')
    location_id = fields.Many2one(comodel_name='stock.location.ept', string='Location',
                                  help='LOcation of the inventory')
    inventory_date = fields.Date(string='Date', help='Date of the inventory.', default=fields.Date.today())
    inventory_line_ids = fields.One2many(comodel_name='stock.inventory.line.ept', inverse_name='inventory_id',
                                         string='Inventory lines',
                                         help='Inventory lines of the inventory')
    stock_move_ids = fields.One2many(comodel_name='stock.inventory.line.ept', inverse_name='inventory_id',
                                     string='Inventory lines',
                                     help='Inventory lines of the inventory')

    def start_inventory(self):
        self.state = 'in-progress'
        print(self.env.context)
        for inventoryline in self.inventory_line_ids:
            inventoryline.available_qty = inventoryline.product_id.with_context(location=self.location_id).product_stock

    def validate_inventory(self):
        location_internal = self.env['stock.location.ept'].search([('location_type', '=', 'Inventory Loss')], limit=1)
        soucre_location = location_internal
        destination_location = self.location_id
        for inventoryline in self.inventory_line_ids.filtered(lambda line: line.difference != 0):
            if inventoryline.difference < 0:
                soucre_location = destination_location
                destination_location = location_internal

            self.env['stock.move.ept'].create({
                'name': inventoryline.product_id.name + '-->' + soucre_location.name + '--->' + destination_location.name,
                'product_id': inventoryline.product_id.id,
                'uom_id': inventoryline.product_id.uom_id.id,
                'source_location_id': soucre_location.id,
                'destination_location_id': destination_location.id,
                'qty_to_deliver': abs(inventoryline.difference),
                'qty_done': abs(inventoryline.difference),
                'state': 'done'})
            print('called')

    def cancel_inventory(self):
        self.state = 'cancelled'
