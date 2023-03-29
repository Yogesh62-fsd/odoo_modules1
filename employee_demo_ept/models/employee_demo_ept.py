# -*- coding: utf-8 -*-
from odoo import  fields, models

class EmployeeDemoEPT(models.Model):
    
     _name = 'employee.demo.ept'
     _description = 'Employee Demo EPT'
     
     name=fields.Char(string='Name', help='Name of the customer')
     email=fields.Char(string='Email', help='Email of the customer')
     phone=fields.Char(string='Phone', help='Phone number of the customer')
     city=fields.Char(string='City', help='City of the customer')
     state=fields.Char(string='State', help='State of the customer')
     country=fields.Char(string='Country', help='Country of the customer')
     description=fields.Char(string='Descripton', help='Descripton of the customer')
     