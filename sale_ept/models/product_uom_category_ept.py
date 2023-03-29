from odoo import models, fields


class ProductUomCategoryEpt(models.Model):
    _name = 'product.uom.category.ept'
    _description = 'Product Uom Category Ept'

    name = fields.Char(string='Product Uom Category Name', help='Name of the Product Uom Category')
    uom_ids=fields.One2many(comodel_name='product.uom.ept',inverse_name='uom_category_id',string='Product Uom Category IDs', help='IDs of the Product Uom Category')