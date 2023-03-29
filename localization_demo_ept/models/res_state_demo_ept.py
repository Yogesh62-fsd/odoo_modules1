# -*- coding: utf-8 -*-

from  odoo import  models,fields

class StateDemoEPT(models.Model):
    _name="res.state.demo.ept"
    _description="State Demo EPT"

    name=fields.Char(string="Name",help="Name of the state")
    code=fields.Char(string='Code',help="Code of the state")
    country_name=fields.Char(string="Country",help="Country of the state",copy=False)
    active=fields.Boolean(string='Active',help="Active field of the state",default=True)