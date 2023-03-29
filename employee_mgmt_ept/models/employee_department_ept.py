from odoo import models, fields


class EmployeeDepEpt(models.Model):
    _name = "employee.department.ept"
    _description = "Employee Department EPT"

    name = fields.Char(string="Department Name", help="Name of employee Department", required=True)
    employees_ids = fields.One2many(comodel_name='employee.ept', inverse_name='department_id', string="Department Employee ids",
                                    help="Employees Ids of Department")
    department_manager = fields.Many2one(comodel_name="res.users", string="Department Manager",
                                         help="Manager of employee Department")
