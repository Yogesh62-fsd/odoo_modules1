from odoo import models, fields

class ProductExt(models.Model):
    _inherit = 'product.product'

    deposit_product_id = fields.Many2one(comodel_name='product.product', string='Deposit Product',
                                         help='Deposit product id of the product')
    deposit_product_qty = fields.Integer(string='Deposited Quantity', help='Deposit product quantity of the product')



