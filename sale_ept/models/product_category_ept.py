
from odoo import models,fields

class ProductCategoryEpt(models.Model):
    _name='product.category.ept'
    _description='Product Category Ept'

    name=fields.Char(string='Product Category Name',help='Category Name of the product',required=True)
    parent_id=fields.Many2one(comodel_name='product.category.ept',string='Parent Product Category ID',help="Parent Product Category of the products")


