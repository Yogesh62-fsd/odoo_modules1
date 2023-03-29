from odoo import models, fields, Command, api


class SaleOrderEpt(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    crm_lead_ept_id = fields.Many2one(comodel_name='crm.lead', string='Lead', help='lead id of the sale order')

    is_all_picking_completed = fields.Boolean(compute='_compute_all_picking_completed',
                                              search='_search_is_all_order_completed', string='All Order Completed',
                                              help='All sale order is completed')
    net_profit_value = fields.Float(string='Net Profit Value', help='Net Profit of this sale order',
                                    compute='_compute_net_profit_value')
    net_profit_margin = fields.Float(string='Net Profit Margin', help='Net Profit Margin of this sale order',
                                     compute='_compute_net_profit_margin')

    product_tmpl_ids = fields.Many2many(comodel_name='product.template', string='Product Template',
                                        help='Product Template ids for the order')

    def _action_confirm(self):
        pass
        # """
        # :param self current record
        # :return: super to parent
        # this method is overriden to add  the product in the orderline ..of the current order
        # # """
        # orderline = []
        # product = self.env.ref('sale_order_extend.product_first')
        # orderline.append(Command.create({'product_id': product.id,
        #                                  'name': product.name,
        #                                  'price_unit': product.lst_price
        #                                  }))
        # self.write({'order_line': orderline})
        return super(SaleOrderEpt, self)._action_confirm()

    def manage_deposit(self):
        """
        :param self current sale order i.e is open in form view.
        :return: nothing
        this method is used to manage deposit product corresponding to the sale order line product .
        here we are checking if any deposit product is found corresponding to that product then it will added and
        when the main product quantity is updated its Quantity also get updated corresponding to same.
        as given in the product.product model to the field deposit_product_qty
        And if the deposit product is already added then it do add against the same product as well.
        """
        for orderline in self.order_line:
            if orderline.product_orderlines_ids:
                orderline.product_orderlines_ids.product_uom_qty = orderline.product_uom_qty * orderline.product_id.deposit_product_qty
            else:
                if orderline.product_id.deposit_product_id:
                    new_product_id = orderline.product_id.deposit_product_id
                    new_orderlines = []
                    new_orderlines.append(Command.create({'product_id': new_product_id.id,
                                                          'name': new_product_id.name,
                                                          'product_uom_qty': orderline.product_uom_qty * orderline.product_id.deposit_product_qty,
                                                          'product_orderline_id': orderline.id}))
                    self.write({'order_line': new_orderlines})

    def confirm_validate(self):
        self.action_confirm()
        self.picking_ids.action_set_quantities_to_reservation()
        self.picking_ids.button_validate()

    def filter_product(self):
        orderline_products_ids = self.order_line.product_id.ids

        all_saleorderline = self.env['sale.order.line'].search(
            [('order_id', '!=', self.id), ('product_id', 'in', orderline_products_ids),
             ('move_ids.move_line_ids.state', 'not in', ['done', 'cancel']),
             ('move_ids.move_line_ids.product_uom_qty', '>', 0)]).ids

        action = self.env["ir.actions.act_window"]._for_xml_id('sale_order_extend.action_sale_order_line')
        action['domain'] = [('id', 'in', all_saleorderline)]
        return action

    def _compute_all_picking_completed(self):
        for order in self:
            order.is_all_picking_completed = True if len(
                order.picking_ids.search([('sale_id', '=', order.id)]).filtered(
                    lambda picking: picking.state in ['done', 'cancel']).ids) == len(
                order.picking_ids.search([('sale_id', '=', order.id)]).ids) else False

    def _search_is_all_order_completed(self, operator, value):
        """
        the query written below is is getting the sale order id . function except is used to filter those record which are not done and cancel from the all the picking related to that sale order.
        :return: it is return in the domain which contain only those saleorder id which are done or cancelled fully .
        """
        query = "select id from sale_order where id in ((select sale_id from stock_picking) except (select sale_id from stock_picking where state not in ('done','cancel'))) "
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        domain = [('id', 'in', res)]
        return domain

    @api.depends('order_line')
    def _compute_net_profit_value(self):
        for order in self:
            order.net_profit_value = sum([orderline.profit_value for orderline in order.order_line])

    @api.depends('order_line')
    def _compute_net_profit_margin(self):
        for order in self:
            total_cost = sum([orderline.cost_price * orderline.product_uom_qty for orderline in order.order_line])
            total_cost = 1 if total_cost == 0 else total_cost
            order.net_profit_margin = (order.net_profit_value / total_cost) * 100

    @api.onchange('product_tmpl_ids')
    def onchange_product_temp_ids(self):
        new_orderlines = []
        template_products = self.product_tmpl_ids.product_variant_ids.filtered(
            lambda product: product.ids[0] not in self.order_line.product_id.ids)
        for products in template_products:
            if self.env['stock.quant'].search(
                    [('location_id', '=', self.warehouse_id.lot_stock_id.id), ('product_id', '=', products.ids[0]),
                     ('available_quantity', '>', 0)]):
                new_orderlines.append(Command.create({'product_id': products.ids[0],
                                                      'name': products.name,
                                                      'price_unit': products.lst_price
                                                      }))
        self.write({'order_line': new_orderlines})
        [orderline.product_id_change() for orderline in self.order_line]

        # for orderline in self.order_line:
        #     if orderline.product_id.id not in self.product_tmpl_ids.product_variant_ids.ids:
        #         self.write({'order_line': [Command.delete(orderline.id)]})

        [self.write({'order_line': [Command.delete(orderline.id)]}) for orderline in self.order_line if
         orderline.product_id.id not in self.product_tmpl_ids.product_variant_ids.ids]
        [orderline.product_id_change() for orderline in self.order_line]


