# -*- coding: utf-8 -*-
from odoo import models,fields

class PartnerDemoEPT1(models.Model):
  _name="res.partner.demo.ept1"
  _description = "Partner Demo EPT1"




  name=fields.Char(string='Name',help='Name of the contact')
  email=fields.Char(string='Email',help='Email of the contact')
  street1=fields.Char(string='Street1',help='Street1 of the contact')
  street2 = fields.Char(string='Street2', help='Street2 of the contact')
  city=fields.Char(string='City',help='city of the contact')
  state = fields.Char(string='State', help='state of the contact')
  zipcode = fields.Char(string='Zipcode', help='zipcode of the contact')
  country = fields.Char(string='Country', help='Country of the contact')
  birthdate=fields.Date(string='Birthdate',help='Birthdate of the contact')
  age=fields.Integer(string='Age',help='Age of the contact')
  weight=fields.Float(string='Weight',help='Weight of the contact')
  description=fields.Text(string='Description',help='Description of the contact')
  gender=fields.Selection(string='Gender',selection=[('Male','Male'),('Female','Female'),('Transgender','Transgender')],help='Gender of the contact')
  details=fields.Html(string='Details',help='Details of the contact')
  is_spectacles=fields.Boolean(string='Is_spectacles',help='Is_spectacles of the contact')
  photo=fields.Image(string='Photo',help='Photo of the contact')

  country_name = fields.Char(string='Country', help='Country of the contact')
  country_id=fields.Many2one(comodel_name="res.country.demo.ept",string='Country Id', help='Country Id of the contact')
  parent_id=fields.Many2one(comodel_name="res.partner.demo.ept1",string="Parent Id",help="Parent id of the contact")
  child_ids=fields.One2many(comodel_name="res.partner.demo.ept1",inverse_name="parent_id",string="Child ID")




































































