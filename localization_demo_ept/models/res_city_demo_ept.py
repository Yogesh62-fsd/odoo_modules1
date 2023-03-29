# -*- coding: utf-8 -*-

from odoo import models,fields

class CityDemoEpt(models.Model):
    _name="res.city.demo.ept"
    _description="City Demo EPT"

    name=fields.Char(string="Name",help="Name of the City")
    state_name=fields.Char(string="State Name",help="State Name of the City",copy=False)
    active=fields.Boolean(string="Active",help="Active field  of the City",default=True)
