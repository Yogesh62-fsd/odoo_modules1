from odoo import models, fields
from datetime import date


class CrmLeadDemoEpt(models.Model):
    _name = "crm.lead.demo.ept"
    _description = "CRM Lead Demo Ept"

    name = fields.Char(string="Name", help="Name of the customer",required=True)
    customer_email = fields.Char(string="Email", help="Email of the customer",required=True)
    customer_phone = fields.Char(string="Phone", help="Phone of the customer",required=True)
    expected_revenue = fields.Float(string="Revenue", help="Revenue of the customer")
    sales_person = fields.Char(string="Sales Person", help="Sales Person of the customer", required=True)
    sales_team = fields.Char(string="Sales Team", help="Sales Team of the customer")
    campaign = fields.Char(string="Campaign", help="Campaign of the customer")

    channel = fields.Selection(string="Channel",
                               selection=[('Facebook', 'Facebook'), ('WhatsApp', 'WhatsApp'), ('Email', 'Email'),
                                          ('Newspaper', 'Newspaper'), ('Television', 'Television'), ('Phone', 'Phone'),
                                          ('Call', 'Call'), ('SMS', 'SMS'), ('Google Ads', 'Google Ads')],
                               required=True, help="Channel of the customer")

    state = fields.Selection(string="State",
                             selection=[('New', 'New'), ('Qualified', 'Qualified'), ('Proposition', 'Proposition'),
                                        ('Won', 'Won'), ('Lost', 'Lost')], widget='statusbar', clickable=True,
                             default='New', help="State of the customer")

    next_followup_date = fields.Date(string="Follow up Date", required=True, default=date.today(),
                                     help='Follow up Date of the Customer')
    won_date = fields.Date(string="Won Date", help='WON Date of the Customer')
    lost_reason = fields.Text(string='Lost Reason', help="Lost Reason of the Customer")
