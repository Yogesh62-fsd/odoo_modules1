# -*- coding: utf-8 -*-

from odoo import models, fields


class PartnerDemoEpt2(models.Model):
    _name = "res.partner.demo.ept2"
    _description = "Partner Demo EPT2"

    name = fields.Char(string="Name", help="Name of the contact")
    email = fields.Char(string="Email", help="Email of the contact")
    street1 = fields.Char(string="Street1", help="Street1 of the contact")
    street2 = fields.Char(string="Street2", help="Street2 of the contact")
    city=fields.Char(string="City",help="City of the contact")
    state=fields.Char(string="State",help="State of the contact")
    zipcode=fields.Char(string="Zipcode",help="Zipcode of the contact")
    country=fields.Char(string="Country",help="Country of the contact")
    birthdate=fields.Date(string="Birthdate",help="Birthdate of the contact")
    age=fields.Integer(string="Age",help="Age of the contact")
    gender=fields.Selection(string='Gender',selection=[('Male','Male'),('Female','Female'),('Transgender','Transgender')])
    is_spectacles=fields.Boolean(string="Is_spectacles",help="Spectacles of the contact")
    photo=fields.Image(string="Photo",help="Photo of the contact")
    details=fields.Html(string="Details",help="Details of the contact")
    weight=fields.Float(string="Weight",help="Weight of the contact")
    description=fields.Text(string="Description",help="Description of the contact")