from odoo import models,fields,api
from odoo.exceptions import ValidationError

class StateEPT(models.Model):
    _name="res.state.ept"
    _description="State EPT"

    name=fields.Char(string="State Name" ,help="Name of the State")
    code=fields.Char(string="State Code" ,help="Code of the State")
    country_id=fields.Many2one(comodel_name="res.country.ept",string=" State Country Id" ,help="Country Id of the State")
    city_ids=fields.One2many(comodel_name="res.city.ept",inverse_name="state_id",string="State City Ids" ,help="State City Ids of the State")

    @api.constrains('code')
    def unique_state_code(self):  # applying unique constraint for state code .... using python constraints.

        # print(len(self.search([('code','=',self.code)]).mapped('code')))

        if len(self.search([('code','=',self.code)]).mapped('code'))>1:

              unique_record=set(self.search([('code','=',self.code)]).mapped('code'))
              print(unique_record) # for demo only
              raise ValidationError('Warning: State Code is Must be unique.')
