from odoo import models,fields,api

class PurchaseOrderLineEpt(models.Model):
    _name='purchase.order.line.ept'
    _description='Purchase OrderLine Ept'

    name = fields.Char(string='Description', help='Description of the Purchase order line product')
    purchase_order_id=fields.Many2one(comodel_name='purchase.order.ept',string='Purchase Order id',help='Order id of the Purchase orderline')
    product_id=fields.Many2one(comodel_name='product.ept',string='Product',help='Product of the Purchase Order Line')

    quantity= fields.Float(string='Quantity',digits=(6,2), help='Purchase Quantity of the purchase orderline product')
    cost_price=fields.Float(string='Cost Price', default='1.00', help='Cost Price of the purchase orderline proudct ')
    state=fields.Selection(string='State',selection=[('draft', 'draft'),('confirm','confirm'), ('done', 'done'), ('cancelled', 'cancelled')],help='State of the Purchase Order line')
    uom_id=fields.Many2one(comodel_name='product.uom.ept',string='UOM Id',help='Uom Id of Purchase order line')

    @api.onchange('product_id')
    def onchange_name(self):
        self.name = self.product_id.description
        self.uom_id=self.product_id.uom_id.id
        self.cost_price = self.product_id.cost_price
        self.state='draft'

