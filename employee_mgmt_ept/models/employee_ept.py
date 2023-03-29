
from odoo import models,fields

class EmployeeEPT(models.Model):
    _name='employee.ept'
    _description='Employee EPT'

    name=fields.Char(string='Employee Name',help='Name of the Employee',required=True)
    department_id=fields.Many2one(comodel_name='employee.department.ept',string='Employee Department',help='Department Name of the Employee',required=True)
    shift=fields.Many2one(comodel_name='employee.department.shift.ept',string='Employee Shift ',help='Shift of the Employee',required=True)
    job_position=fields.Char(string='Employee JOb Position',help='Job Position of the Employee')
    salary=fields.Float(string='Employee Salary',help='Salary of the Employee',digits=(6,2))
    hire_date=fields.Date(string='Employee Hire Date',help='Hire Date of the Employee')
    gender=fields.Selection(string='Gender',selection=[('Male','Male'),('Female','Female'),('Transgender','Transgender')],help="Gender of the contact")
    job_type=fields.Selection(string='Employee JOb Type',selection=[('Permanent','Permanent'),('AdHoc','AdHoc')],help='Gender of the employee')
    is_manager=fields.Boolean(string='Employee Is Manager',help='Employee is manager in comapany')
    manager_id=fields.Many2one(comodel_name='employee.ept',string='Employee Manger',help='Manager of the Employee')
    related_user=fields.Many2one(comodel_name="res.users", string="Related User",help="Manager of employee")
    # one2 many with self
    employee_ids=fields.One2many(comodel_name='employee.ept',inverse_name='manager_id',string=' Manger Employee Id',help='Manager Employees IDs of the Employee',readonly=True)
    increment_percentage=fields.Float(string='Manager Increment Percentage',help='Salary of the Employees Manger')













