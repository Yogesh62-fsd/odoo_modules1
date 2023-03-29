from odoo import models,fields
class EmployeeLeaveEPT(models.Model):
    _name='employee.leave.ept'
    _description=' Employee Leave EPT'

    employee=fields.Many2one(comodel_name='employee.ept',string='Employee',help=' Leave  of Employee')
    department=fields.Many2one(comodel_name='employee.department.ept',related='employee',store=False,readonly=True)
    start_date=fields.Date(string='Leave Start Date',help='Employee leave start date')
    end_date=fields.Date(string='Leave End Date',help='Employee leave end date')
    state=fields.Selection(string='Employee Status',selection=[('Draft','Draft'),('Approved','Approved'),('Refused','Refused'),('Cancelled','Cancelled')],default='Draft',widget='statusbar')
    leave_description=fields.Text(string='Leave Description',help='Employee leave description',required=True)
    name=fields.Char(related='employee.name',string='Employee Name',help='Name of the employee on leave')

# employee.department_name.department_manager.id=user.id
# employee.department.department_manager.id = user.id