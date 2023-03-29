from odoo import models,fields

class CourseEPT(models.Model):
    _name="course.ept"
    _description="Course Demo EPT"

    name = fields.Char(string="Course Name", help="Name of the Course",required=True)
    student_ids=fields.Many2many(comodel_name="student.ept",string="Student ids Courses ", help="Student  ids of the Course")
