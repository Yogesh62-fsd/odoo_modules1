from odoo import models,fields

class ProductUomEpt(models.Model):
    _name='product.uom.ept'
    _description='Product Uom EPT'


    name=fields.Char(string='Product Uom Category Name',help='Name of the Product Uom Category')
    uom_category_id=fields.Many2one(comodel_name='product.uom.category.ept',string='Product Uom Category id',help='ID of the Product Uom Category')



