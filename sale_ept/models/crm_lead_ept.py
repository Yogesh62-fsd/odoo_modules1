from odoo import models, fields
from odoo import Command, api
from odoo.exceptions import ValidationError


class CrmLeadEPT(models.Model):
    _name = 'crm.lead.ept'
    _description = 'Crm Lead Ept'

    name = fields.Char(string='LeadNo', help='Lead no of the crm lead ept.', readonly=True)
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string='Partner Name', help='Name of the Partner')
    order_ids = fields.One2many(comodel_name='sale.order.ept', inverse_name='lead_id', string='Orders', readonly=True,
                                help='orders of the Partner')
    team_id = fields.Many2one(comodel_name='crm.team.ept', string='Team Leader', help='Team Leader of the lead')
    user_id = fields.Many2one(comodel_name='res.users', string='Saleperson', help='Sale person of crm lead')
    lead_line_ids = fields.One2many(comodel_name='crm.lead.line.ept', inverse_name='lead_id', string='Lead lines ids',
                                    help='Lead lines ids of crm lead')
    state = fields.Selection(string='Lead State',
                             selection=[('New', 'New'), ('Qualified', 'Qualified'),
                                        ('Proposition', 'Proposition'), ('Won', 'Won'), ('Lost', 'Lost')],
                             help=' Lead State of the crm lead ept', default='New')

    won_date = fields.Date(readonly=True, string='Lead Won Date', help='Won Date of the lead')
    lost_reason = fields.Text(string='Lead Lost Reason', help='Lost Reason of the lead ept')
    next_followup_date = fields.Date(string='Lead Next Followup Date', help='Next Followup Date of the lead')

    partner_name = fields.Char(string='Partner Name', help='Name of the Partner')
    partner_email = fields.Char(string='Partner Email', help='Name of the Partner')
    partner_country_id = fields.Many2one(comodel_name='res.country.ept', string='Partner Country',
                                         help='Country of the Partner')
    partner_state_id = fields.Many2one(comodel_name='res.state.ept', string='Partner State',
                                       help='state of the Partner')
    partner_city_id = fields.Many2one(comodel_name='res.city.ept', string='Partner City', help='city of the Partner')

    def change_state(self):

        if self.state == 'New':
            self.state = 'Qualified'
        elif self.state == 'Qualified':
            self.state = 'Proposition'

        print('change_state called')

    def change_state_won(self):
        self.state = 'Won'
        self.won_date = fields.Date.today()
        print('change_state to Won')

    def change_state_lost(self):
        self.state = 'Lost'
        print('change_state to Lost')

    def generate_new_customer(self):

        partner = self.env['res.partner.ept'].create({'name': self.partner_name,
                                                      'email': self.partner_email,
                                                      'country': self.partner_country_id.id,
                                                      'state': self.partner_state_id.id,
                                                      'city': self.partner_city_id.id})
        self.partner_id = partner
        # print('Customer created')

    def generate_quotation(self):

        if self.partner_id:
            order = self.env['sale.order.ept']
            orderline = self.env['sale.orderline.ept']
            orderlines = []

            for leadline in self.lead_line_ids:
                orderlines.append(Command.create(
                    {'product_id': leadline.product_id.id, 'unit_price': leadline.product_id.sale_price,
                     'quantity': leadline.expected_sell_qty,
                     'subtotal_without_tax': orderline.subtotal_without_tax}))

            temporder = order.new({'customer_id': self.partner_id})
            temporder.onchange_customer_id()

            order.create({'customer_id': self.partner_id.id,
                          'invoice_customer_id': temporder.invoice_customer_id.id,
                          'shipping_customer_id': temporder.shipping_customer_id.id,
                          'state': 'draft',
                          'order_line_ids': orderlines,
                          'sales_person_id': self.user_id.id,
                          'lead_id': self.id})


        else:

            raise ValidationError('Warning: Please Select the Customer Before genrating the Quotation.')
            print('Quotation created')

    @api.model
    def create(self, vals):  # getting  the sequence for the name field .
        vals['name'] = self.env['ir.sequence'].next_by_code('sequence.crm.lead.ept')
        # print('create is called.............',vals['name'])
        return super(CrmLeadEPT, self).create(vals)
