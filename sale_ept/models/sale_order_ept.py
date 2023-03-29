from odoo import models, fields
from odoo import api, Command

from odoo.exceptions import ValidationError


class SaleOrderEpt(models.Model):
    _name = 'sale.order.ept'
    _description = 'Sale Order Ept'

    name = fields.Char(string='Sale Order Number', help='Order Number of Sale Order', readonly=True)
    customer_id = fields.Many2one(comodel_name='res.partner.ept', string='Customer Sale Order ',
                                  help=' Customer Id  Order  of Sale Order')
    invoice_customer_id = fields.Many2one(comodel_name='res.partner.ept', string=' Customer Invoice',
                                          help='Customer Invoice of the Sale order')
    shipping_customer_id = fields.Many2one(comodel_name='res.partner.ept', string=' Customer Shipping',
                                           help='Customer Invoice of the Sale order')

    sale_order_date = fields.Date(string='Sale order Date', help='Order Date of Sale Order',
                                  default=fields.Date.today())
    order_line_ids = fields.One2many(comodel_name='sale.orderline.ept', inverse_name='order_id',
                                     string='Sale Order Number', help='Order Number of Sale Order')
    sales_person_id = fields.Many2one(comodel_name='res.users', string='Sale Order User', help='User of the Sale order')
    state = fields.Selection(string='State Sale Order',
                             selection=[('draft', 'draft'), ('confirmed', 'confirmed'), ('done', 'done'),
                                        ('cancelled', 'cancelled')], help='State of the Sale order')
    total_weight = fields.Float(string='Sale Order Product Weight', help='Weight of  Sale Order Product',
                                compute='_compute_total_weight')
    total_volume = fields.Float(string='Saler order Volume', help='Weight of  Sale Order Product',
                                compute='_compute_total_volume')
    order_total = fields.Float(string='Saler Order Total', help='Weight of  Sale Order total',
                               compute='_compute_order_total')

    lead_id = fields.Many2one(comodel_name='crm.lead.ept', string='Saler Order Lead', help='Lead id  of  Sale Order')

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse.ept', string='WareHouse',
                                   help='warehouse id of the sale order.')
    picking_ids = fields.One2many(comodel_name='stock.picking.ept', inverse_name='sale_order_id',
                                  string='Sale Order Number', help='Order Number of Sale Order', readonly=True)
    delivery_count = fields.Float(string="Delivery", compute='_compute_delivery_count')
    stock_move_count = fields.Float(string="Stock Move", compute='_compute_stock_move_count')

    def _compute_total_weight(self):
        # self.total_weight=sum([product.weight for order in self for products in order.order_line_ids.product_id for product in products])  #this only give total weight but not with quantity
        # print(self.total_weight)
        #          or
        for order in self:
            order.total_weight = 0
            for orderline in order.order_line_ids:
                for product in orderline.product_id:
                    order.total_weight += product.weight * orderline.quantity

    def _compute_total_volume(self):  # Calculating the total volume for sale order
        for order in self:
            order.total_volume = 0
            for orderline in order.order_line_ids:
                for product in orderline.product_id:
                    order.total_volume += product.volume * orderline.quantity

    @api.depends('order_line_ids.subtotal_without_tax')
    def _compute_order_total(self):

        for order in self:
            order_total = 0
            for orderline in order.order_line_ids:
                order_total += orderline.subtotal_without_tax
            order.order_total = order_total

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if not self.customer_id.child_ids:
            self.invoice_customer_id = self.shipping_customer_id = self.customer_id
        else:
            invoice_customers = self.customer_id.child_ids.filtered(lambda childs: childs.address_type == 'Invoice')

            shipping_customers = self.customer_id.child_ids.filtered(lambda childs: childs.address_type == 'Shipping')

            self.invoice_customer_id = invoice_customers[0].id
            self.shipping_customer_id = shipping_customers[0].id

    @api.model
    def create(self, vals):  # getting  the sequence for the name field .
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.sale.order.ept')
        return super(SaleOrderEpt, self).create(vals)

    def confirm_sale_order(self):
        if self.state == 'draft':
            self.state = 'confirmed'

        source_stock = self.warehouse_id.stock_location_id
        destination_customer = self.env['stock.location.ept'].search([('location_type', '=', 'Customer')], limit=1)
        transaction_move_name = source_stock.name + "--->" + destination_customer.name
        if destination_customer:
            orderline_warehouse = {}
            movelines = []
            for saleordeline in self.order_line_ids:
                warehouse_id = saleordeline.warehouse_id.id if saleordeline.warehouse_id else self.warehouse_id.id

                if not orderline_warehouse.get(warehouse_id):
                    orderline_warehouse.update({warehouse_id: []})

                orderline_warehouse[warehouse_id].append(
                    Command.create({'name': saleordeline.product_id.name + "--->" + transaction_move_name,
                                    'product_id': saleordeline.product_id.id,
                                    'uom_id': saleordeline.uom_id.id,
                                    'source_location_id': source_stock.id,
                                    'destination_location_id': destination_customer.id,
                                    'sale_line_id': saleordeline.id,
                                    'qty_to_deliver': saleordeline.quantity,
                                    'qty_done': 0
                                    }))
            for key, val in orderline_warehouse.items():
                self.env['stock.picking.ept'].create({'partner_id': self.customer_id.id,
                                                      'sale_order_id': self.id,
                                                      'transaction_type': 'Out',
                                                      'move_ids': val
                                                      })
        else:
            raise ValidationError('Warning:NO Customer Found Sale order cannot be created.')

    def delivery_order(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale_ept.stock_picking_ept_action2')
        if len(self.picking_ids) > 1:
            action['domain'] = [('id', 'in', self.picking_ids.ids)]
        else:
            form_view = [(self.env.ref('sale_ept.view_stock_picking_ept_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = self.picking_ids.id
        return action

    def stock_moves(self):
        action = self.env['ir.actions.act_window']._for_xml_id('sale_ept.stock_move_ept_action')
        if len(self.picking_ids.move_ids) > 1:
            action['domain'] = [('id', 'in', self.picking_ids.move_ids.ids)]
        else:
            form_view = [(self.env.ref('sale_ept.view_stock_move_ept_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = self.order_line_ids.stock_move_ids.id
        return action

    def _compute_delivery_count(self):
        for delivery in self:
            delivery.delivery_count = len(delivery.picking_ids)

    def _compute_stock_move_count(self):
        for stock_move in self:
            stock_move.stock_move_count = len(stock_move.order_line_ids.stock_move_ids)
