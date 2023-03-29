from odoo import models,fields

class StockInventoryLineEpt(models.Model):
    _name='stock.inventory.line.ept'
    _description='Stock Inventory Line Ept'

    product_id = fields.Many2one(comodel_name='product.ept', string='Product',
                                 help='Product of the Inventory Line')
    available_qty=fields.Float(string='System Quantity',help='Quantity of the Product.',readonly=True)
    counted_product_qty=fields.Float(string='Counted Product',help='Counted product stock in inventory lines')
    difference=fields.Float(string='Inventory Loss',help='Inventory lost  product in inventory lines',compute='_compute_difference')
    inventory_id=fields.Many2one(comodel_name='stock.inventory.ept',string='Inventory Id',help='Inventory id of the inventory lines.')

    def _compute_difference(self):
       for inventoryline in self:
        inventoryline.difference=inventoryline.counted_product_qty-inventoryline.available_qty
