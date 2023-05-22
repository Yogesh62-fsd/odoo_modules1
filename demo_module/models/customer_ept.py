from odoo import models, fields, api


class CustomerEpt(models.Model):

    _name = 'customer.ept'
    _description = 'Customer Ept'

    name = fields.Char(string='Name', help='name of the customer')
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), (
        'female', 'Female'), ('transgender', 'Transgender')], help='gender of the customer')
    email = fields.Char(string='Email', help='email of the customer')
    mobile_no = fields.Integer(
        string="Mobile No", help='mobile no of the customer')
    city = fields.Char(string="City", help='City of the customer')
    state = fields.Char(string='State', help='state of the customer')
    country = fields.Char(string='Country', help='country of the customer')
    pincode = fields.Integer(string='Pincode', help='pincode of the customer')

    parent_id = fields.Many2one(
        comodel_name='customer.ept', string='Parent', help='parent id of the customer.')
    child_ids = fields.One2many(comodel_name='customer.ept', inverse_name='parent_id',
                                string='Child Customer', help='Child ids of the customer')
    child_count = fields.Integer(
        string='Childs', compute='_compute_childs_count')

    def _compute_childs_count(self):
        for child in self:
            child.child_count = len(child.child_ids)

    @api.depends('child_ids')
    def action_open_childs(self):

        action = self.env['ir.actions.act_window']._for_xml_id(
            'demo_module.customer_ept_action')

        if (len(self.child_ids) > 1):
            action['domain'] = [('id', 'in', self.child_ids.ids)]
        else:
            form_view = [
                (self.env.ref('demo_module.view_customer_ept_form').id, 'form')]

            action['views'] = form_view
            action['res_id'] = self.child_ids.id
        return action
