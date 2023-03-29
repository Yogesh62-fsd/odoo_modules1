from odoo import models, fields


class EmployeeDemoEpt(models.Model):
    _name = "employee.demo.ept"
    _description = "Employee Demo EPT"

    name = fields.Char(string="Name", help="Name of the Employee")
    department_name = fields.Char(string="Department Name", help="Department Name of the Employee")
    job_position=fields.Char(string="Job Postion", help="Job Postion of the Employee")
    salary=fields.Float(string="Salary",digits=(6,2), help="Salary of the Employee")
    hire_date=fields.Date(string="Hiring Date", help="Hiring Date of the Employee")
    gender=fields.Selection(string="Gender",selection=[('Male','Male'),('Female','Female'),('Transgender','Transgender')],help='Gender of the contact')
    job_type=fields.Selection(string="Job Type",selection=[('Permanent','Permanent'),('ADHoc','ADHoc')])

