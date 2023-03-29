from odoo import models, fields


class EmployeeDepShifEpt(models.Model):
    _name = "employee.department.shift.ept"
    _description = "Employee Department Shift EPT"


    shift = fields.Selection(string='Employee Shift',
                             selection=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'),
                                        ('Night', 'Night')])
    _rec_name='shift'

