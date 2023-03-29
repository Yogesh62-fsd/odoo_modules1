# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductDemoEPT(models.Model):
    _name = "res.product.demo.ept"
    _description = "Product Demo EPT"

    name = fields.Char(string="Name", help="Name of the product")
    default_code = fields.Char(string="SKU Code", help="Product SKU Code of the product")
    barcode = fields.Char(string="Barcode", help="Barcode of the product")
    can_sold = fields.Boolean(string="Sold", help="Selling   of the product")
    product_type = fields.Selection(string="Product Type",
                                    selection=[('Stockable', 'Stockable'), ('Consumable', 'Consumable'),
                                               ('Service', 'Service')])
    sale_price = fields.Float(string="Selling Price",digits=(6,2), help="Selling Price  of the product")
    cost_price = fields.Float(string="Cost Price",digits=(6,2) ,help="Cost Price  of the product")
    active = fields.Boolean(string="Active", help="Active field of the product", default=True)
    warehouse = fields.Char(string="Warehouse", help="Warehouse of the product")
    product_image = fields.Image(string="Image", help="Image of the product")
    website_description = fields.Html(string="Description",default="this is product description", help="Description of the product")
    internal_note = fields.Text(string="Note",default="this is product note", help="Note of the product")
