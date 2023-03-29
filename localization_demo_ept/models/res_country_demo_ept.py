# -*- coding: utf-8 -*-
from odoo import models,fields

class CountryDemoEPT(models.Model):
    _name="res.country.demo.ept"
    _description="Country Demo Ept"

    name=fields.Char(string="Name",help="Name of the country.")
    code=fields.Char(string="Code",help="Code of the country.")
    active=fields.Boolean(string="Active",help="Active of the country.",default='True')

    # partner_id=fields.One2many(comodel_name="res.partner.demo.ept1",inverse_name="country_id",string="Partner ",help="Partner id of the customer")



