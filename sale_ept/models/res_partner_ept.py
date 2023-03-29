from odoo import models, fields
from odoo import Command


class PartnerEPT(models.Model):
    _name = 'res.partner.ept'
    _description = 'Partner EPT'

    name = fields.Char(string='Name', help='Name of the Customer')
    street1 = fields.Char(string='Street1', help='Street1 of the Customer')
    street2 = fields.Char(string='Street2', help='Street2 of the Customer')
    country = fields.Many2one(comodel_name='res.country.ept', string='Country', help='Country of the Customer')
    state = fields.Many2one(comodel_name='res.state.ept', string='State', help='state of the Customer')
    city = fields.Many2one(comodel_name='res.city.ept', string='City', help='city of the Customer')
    zip_code = fields.Char(string='Zipcode', help='zipcode of the Customer')
    email = fields.Char(string='Email', help='Email of the Customer')
    mobile = fields.Char(string='Mobile', help='state of the Customer')
    phone = fields.Char(string='Phone', help='state of the Customer')
    photo = fields.Image(string='Photo', help='Photo of the Customer')
    website = fields.Char(string='Website', help='Website of the Customer')
    active = fields.Boolean(string='Active', default=True, help=' Active Field of the Customer')
    parent_id = fields.Many2one(comodel_name='res.partner.ept', string='Parent Id', help='Parent Id of the Customer')
    child_ids = fields.One2many(comodel_name='res.partner.ept', inverse_name='parent_id', string='Child Customers',
                                help='Child ids of the Customer')
    address_type = fields.Selection(string='Address Type',
                                    selection=[('Invoice', 'Invoice'), ('Shipping', 'Shipping'),
                                               ('Contact', 'Contact')],
                                    help='Address Type  of the Customer')

    def create_partners(self):
        self.write({'name': 'Somesh Sukla',
                    'email': 'sarthak@dummy.com',
                    'mobile': 90876545,
                    'child_ids': [Command.update(self.child_ids[0].id, {'name': 'Aman Pandey'}),
                                  Command.create(
                                      {'name': 'Kamlesh Ashtik', 'email': 'kamlesh@dummy.com', 'mobile': 90876545, }),

                                  ]
                    })
        print(self.child_ids[0].id)

    def create_orders(self):
        orderlineobj = self.env['sale.orderline.ept']
        productsobj = self.env['product.ept']
        products = productsobj.search([])

        orderlines = []
        for product in products:
            # print(product.name)
            orderlines.append(Command.create(
                {'product_id': product.id, 'unit_price': product.sale_price, 'quantity': 10,
                 'subtotal_without_tax': orderlineobj.subtotal_without_tax}))

        # print(orderlines)
        order = self.env['sale.order.ept']
        order_id = order.create(
            {'name': order.name, 'customer_id': self.id, 'state': 'draft', 'order_line_ids': orderlines})


        orderlines.append(Command.update(order_id.order_line_ids[0].id,{ 'unit_price': 560,'quantity': 10,}))

        order_id.write({'order_line_ids':orderlines})

    #      print(orderlines)
    #      order.write({'order_line_ids': orderlines})
    # # print('this is called ')
