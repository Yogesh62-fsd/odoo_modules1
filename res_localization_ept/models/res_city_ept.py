
from  odoo import  models,fields

class CityEpt(models.Model):

    _name="res.city.ept"
    _description="City EPT"

    name=fields.Char(string="City Name",help="Name of the City")
    state_id=fields.Many2one(comodel_name="res.state.ept",string="City State id",help="State Id of the City")