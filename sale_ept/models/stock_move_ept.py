from odoo import models, fields


class StockMoveEpt(models.Model):
    _name = 'stock.move.ept'
    _description = 'Stock Move Ept'

    name = fields.Char(string='Description', help='Name of the Move Location')
    product_id = fields.Many2one(comodel_name='product.ept', string='Product Name', help='Name of the product',
                                 required=True)
    uom_id = fields.Many2one(comodel_name='product.uom.ept', string='Uom_id', help='UOm id of the product',
                             required=True)
    source_location_id = fields.Many2one(comodel_name='stock.location.ept', string='Source Location',
                                         help='Source Location of the stock')
    destination_location_id = fields.Many2one(comodel_name='stock.location.ept', string='Destination Location',
                                              help='Destination Location of the stock')
    qty_to_deliver = fields.Float(string='Demand', help='Quantity to deliver of the product', readonly=True)
    qty_done = fields.Float(string='Done Quantities', help='Done quantity of the product')
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')],
                             help='State of the Sale order', default='draft')
    sale_line_id = fields.Many2one(comodel_name='sale.orderline.ept', string='Sale Orderline',
                                   help='Sale order line ids of the stock ')
    purchase_line_id=fields.Many2one(comodel_name='purchase.order.line.ept',string='Sale Orderline',help='Sale order line ids of the stock ')
    stock_inventory_id=fields.Many2one(comodel_name='stock.inventory.ept',string='Inventory Stock',help='Sale order line ids of the stock ')
    picking_id=fields.Many2one(comodel_name='stock.picking.ept',string='Picking Id',help='Picking id  of the stock ')

