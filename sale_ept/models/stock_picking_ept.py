from odoo import models, fields, api,Command
from odoo.exceptions import  ValidationError


class StockPickingEpt(models.Model):
    _name = 'stock.picking.ept'
    _description = 'Stock Picking Ept'

    name = fields.Char(string='Picking Location Name', help='Name of the Picking Location')
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string='Shipping Partner',
                                 help='Shipping Partner of the picking')
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')],
                             help='State of the Sale order', default='draft')
    sale_order_id = fields.Many2one(comodel_name='sale.order.ept', string='Sale Order',
                                    help='Sale Order of the picking')
    purchase_order_id = fields.Many2one(comodel_name='purchase.order.ept', string='Purchase Order',
                                        help='Sale Order of the picking')
    transaction_type = fields.Selection(string='Transaction Type', selection=[('In', 'In'), ('Out', 'Out')],
                                        help='Transaction type of the Stock picking')
    move_ids = fields.One2many(comodel_name='stock.move.ept', inverse_name='picking_id', string='Move Ids',
                               help='Mover Ids of the picking')
    transaction_date = fields.Date(string='Transaction Date', help='Date of the Transaction ',
                                   default=fields.Date.today())

    back_order_id = fields.Many2one(comodel_name='stock.picking.ept', string='Back Order',
                                    help='Backing Order of the picking')

    @api.model
    def create(self, vals):

        if vals['transaction_type'] == 'In':
            vals['name'] = self.env['ir.sequence'].next_by_code('seq.stock.picking.in.ept')
        elif vals['transaction_type'] == 'Out':
            vals['name'] = self.env['ir.sequence'].next_by_code('seq.stock.picking.out.ept')
        return super(StockPickingEpt, self).create(vals)

    def validate_order(self):
        new_move_lines = []
        moves_to_unlink=[]
        if sum(self.move_ids.mapped('qty_done')) == 0:
            raise ValidationError("No items to process, cannot complete the transaction")

        for stockmove in self.move_ids:
            stockmove.state="done"
            if stockmove.qty_done == 0:
                stockmove.state = "draft"
                moves_to_unlink.append(stockmove.id)
                new_move_lines.append(Command.unlink(stockmove.id))
            elif stockmove.qty_to_deliver - stockmove.qty_done > 0:
                new_move_lines.append(Command.create({ 'name':stockmove.name ,
                                                  'product_id':stockmove.product_id.id,
                                                  'uom_id':stockmove.uom_id.id,
                                                  'source_location_id':stockmove.source_location_id.id,
                                                  'destination_location_id':stockmove.destination_location_id.id,
                                                  'purchase_line_id':stockmove.purchase_line_id.id,
                                                  'qty_to_deliver':stockmove.qty_to_deliver - stockmove.qty_done,
                                                  'sale_line_id':stockmove.sale_line_id.id,
                                                  'qty_done':0
                                                 }))

        if new_move_lines:
            back_order = self.create({'partner_id': self.partner_id.id,
                         'transaction_type': self.transaction_type,
                         'move_ids': new_move_lines,
                         'back_order_id': self.id
                         })
            self.state = "done"
            for move_id in moves_to_unlink:
                back_order.write({'move_ids':[Command.link(move_id)]})
        self.state='done'

    def cancel_order(self):
        for stockmove in self.move_ids:
            stockmove.state = 'cancelled'
            stockmove.qty_done = stockmove.qty_to_deliver
        self.state = 'cancelled'
