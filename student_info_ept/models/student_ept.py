from odoo import models, fields


class StudentEPT(models.Model):
    _name = "student.ept"
    _description = "Student EPT"

    name = fields.Char(string="Student Name", help="Name of the Student")
    student_class = fields.Char(string="Student Class", help="Class of the Student")
    date_of_birth = fields.Date(string="Student DOB", help="Date of Birth  of the Student", required=True)
    course_ids = fields.Many2many(comodel_name='course.ept',string="Student Courses", help="Courses of the Student")
