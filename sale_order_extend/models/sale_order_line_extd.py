from odoo import models, fields, api


class SaleOrderEpt(models.Model):
    _inherit = "sale.order.line"

    product_orderline_id = fields.Many2one(comodel_name='sale.order.line', string='Product Orderline',
                                           help='Order line id corresponding to this product.')

    product_orderlines_ids = fields.One2many(comodel_name='sale.order.line', inverse_name='product_orderline_id',
                                             string='Product Orderline Ids',
                                             help='orders of the Partner')
    cost_price = fields.Float(string='Cost Price', help='Cost Price of the product selected', default=1)
    profit_value = fields.Float(string='Profit Value', help='Profit for this sale order line ',
                                compute='_compute_profit_value')
    warehouse_ept_id = fields.Many2one(comodel_name='stock.warehouse', string='Orderline Warehouse',
                                       help='Warehoues id of the orderline.')
    history_unit_price = fields.Float(string='History Unit Price',
                                      help='History Price of the product selected', default=0)

    #     here field product_orderline_id is kept to store the orderline id of that orderline which
    #     is added due to this current orderline.
    #     like for an example if there product 'A' and there is deposit product 'B' corresponding to it
    #     Now whenever product 'A' is added in the orderline when manage_deposit button is clicked then this
    #     deposit product corresponding to it is also added as in the orderline so identify that this orderline is added
    #     corresponding to this Current Orderline we have kept field."""

    #   here  field product_orderlines_ids is taken to check if the deposit product correspoinding to product that is
    #   added in the orderline is already added and it also help to updadte the qty of product.
    @api.onchange('product_id')
    def product_id_change(self):
        if self.product_id:
            res = super(SaleOrderEpt, self).product_id_change()
            self.cost_price = self.product_id.standard_price
            return res

    @api.depends('product_uom_qty')
    def _compute_profit_value(self):
        for orderline in self:
            orderline.profit_value = (orderline.price_unit - orderline.cost_price) * orderline.product_uom_qty

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderEpt, self)._prepare_procurement_values(group_id)
        if self.warehouse_ept_id:
            values.update({'warehouse_id': self.warehouse_ept_id})
        return values

    @api.onchange('product_id')
    def onchange_history_unit_price(self):
        if self.product_id:
            orderline = self.env['sale.order.line'].search(
                [('order_partner_id', '=', self.order_id.partner_id.id), ('product_id', '=', self.product_id.id),
                 ('state', '=', 'sale')])
            if orderline:
                self.history_unit_price = orderline[0].price_unit
