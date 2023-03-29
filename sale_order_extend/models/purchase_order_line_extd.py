from odoo import models, fields, api


class PurchaseOrderLineExtd(models.Model):
    _inherit = 'purchase.order.line'

    history_unit_price = fields.Float(string='History Unit Price', help='History Price of the product selected')

    @api.onchange('product_id')
    def onchange_history_unit_price(self):
        if self.product_id:
            purchaseorderline = self.env['purchase.order.line'].search(
                [('order_id.partner_id', '=', self.order_id.partner_id.id), ('product_id', '=', self.product_id.id),
                 ('state', '=', 'purchase')])
            if purchaseorderline: self.history_unit_price = purchaseorderline[0].price_unit
