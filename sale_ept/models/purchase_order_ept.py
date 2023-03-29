from odoo import models, fields, api
from odoo import Command
from odoo.exceptions import ValidationError

class PurchaseOrderEpt(models.Model):
    _name = 'purchase.order.ept'
    _description = 'Purchase Order Ept'

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse.ept', string='Warehouse',
                                   help='Warehouse  id of the purchase order ')
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string='Purchase Customer ',
                                 help='Customer of the purchase order')
    order_date = fields.Date(string='Date', help='Date of the purchase order',default=fields.Date.today())
    name = fields.Char(string='Purchase Code', help='Purchase code of purchase order', readonly=True)
    state = fields.Selection(string='State', selection=[('Draft', 'Draft'), ('Confirm', 'Confirm'), ('Done', 'Done'),
                                                        ('Cancelled', 'Cancelled')], help='State of the Purchase Order',default='Draft')
    purchase_order_line_ids = fields.One2many(comodel_name='purchase.order.line.ept', inverse_name='purchase_order_id',
                                              string='Purchase Orderlines',
                                              help='Purchase orderlines of the purchase order')

    @api.model
    def create(self, vals):  # getting  the sequence for the name field .
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.purchase.order.ept')
        return super(PurchaseOrderEpt, self).create(vals)

    def confirm_purchase_order(self):
        if self.state == 'Draft':
            self.state = 'Confirm'

        source_vendor=self.env['stock.location.ept'].search([('location_type','=','Vendor')],limit=1)
        destination_stock=self.warehouse_id.stock_location_id
        transaction_name=source_vendor.name+'--->'+destination_stock.name
        movelines = []

        if source_vendor:

            for purchaseline in self.purchase_order_line_ids:
                movelines.append(Command.create({ 'name':purchaseline.name+':-->'+transaction_name,
                                                  'product_id':purchaseline.product_id.id,
                                                  'uom_id':purchaseline.uom_id.id,
                                                  'source_location_id':source_vendor.id,
                                                  'destination_location_id':destination_stock.id,
                                                  'purchase_line_id':purchaseline.id,
                                                  'qty_to_deliver':purchaseline.quantity,
                                                  'qty_done':0
                                                 }))

            pickingobj = self.env['stock.picking.ept']
            pickingobj.create({
                           'partner_id': self.partner_id.id,
                           'purchase_order_id': self.id,
                           'transaction_type': 'In',
                           'move_ids': movelines
                            })
        else:
            raise ValidationError('Warning: No Vendor found  Purchase order cannot created.')