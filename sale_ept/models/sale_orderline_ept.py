from odoo import models, fields
from odoo import api


class SaleOrderLineEpt(models.Model):
    _name = 'sale.orderline.ept'
    _description = 'Sale Order Line EPT'

    order_id = fields.Many2one(comodel_name='sale.order.ept', string='Order no', help='id of sale order line')
    product_id = fields.Many2one(comodel_name='product.ept', string='Sale Order Line Product',
                                 help='Product of the Sale Order Line')
    name = fields.Text(string='Sale Order Line Description', help='Description of the sale order line')
    quantity = fields.Float(string='Quantity', digits=(6, 2), help='Quantity of the Sale Order Line')
    unit_price = fields.Float(string='Unit Price', digits=(6, 2), help='Unit Price of the Sale Order Line')
    state = fields.Selection(string='State Sale Order Line',
                             selection=[('draft', 'draft'), ('confirmed', 'confirmed'), ('cancelled', 'cancelled')],
                             help='State of the Sale order Line')
    uom_id = fields.Many2one(comodel_name='product.uom.ept', string='Uom id', help='id of sale order line')

    stock_move_ids = fields.One2many(comodel_name='stock.move.ept', inverse_name='sale_line_id', string='Stock Moves',
                                     help='Stock Moves ids of the orderlines', readonly=True)
    subtotal_without_tax = fields.Float(string='Subtotal', compute='_compute_total')
    delivered_qty = fields.Float(string='Delivered Quantity', help='Delivered qty of the ordelines',
                                 compute='_compute_delivered_qty', store=False)
    cancelled_qty = fields.Float(string='Cancelled Quantity', help='Cancelled qty of the ordelines',
                                 compute='_compute_cancelled_qty', store=False)
    warehouse_id=fields.Many2one(comodel_name='stock.warehouse.ept',string='Warehouse',help='warehouse of the orderline..')

    @api.depends('unit_price', 'quantity')
    def _compute_total(self):

        for saleorderline in self:
            saleorderline.subtotal_without_tax = saleorderline.quantity * saleorderline.unit_price
    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.unit_price = self.product_id.sale_price
            self.quantity = 1
            self.uom_id = self.product_id.uom_id.id
            self.name = self.product_id.name
    def _compute_delivered_qty(self):
        for ordeline in self:
            ordeline.delivered_qty = sum([stockmoves.qty_done for stockmoves in self.stock_move_ids if stockmoves.state == 'done'])

    def _compute_cancelled_qty(self):
        for ordeline in self:
            ordeline.cancelled_qty = sum([stockmoves.qty_done for stockmoves in self.stock_move_ids if stockmoves.state == 'cancelled'])
