from odoo import models, fields


class ProductEPT(models.Model):
    _name = "product.ept"
    _description = 'Product Ept'

    name = fields.Char(string="Product Name", help='Name of the Product', required=True)
    sku = fields.Char(string="Product SKU", help='stock keeping unit of the Product', required=True)
    weight = fields.Float(string='Product Weight', help='Weight of the proudct')
    length = fields.Float(string='Product Length', help='Length of the proudct')
    volume = fields.Float(string='Product Volume', help='Volume of the proudct',compute='_compute_volume',readonly=True)
    width = fields.Float(string='Product Width', help='Width of the proudct')
    barcode = fields.Char(string="Product Barcode", help='Barcode of the Product')
    product_type = fields.Selection(string="Product Type",
                                    selection=[('Stockable', 'Stockable'), ('Consumable', 'Consumable'),
                                               ('Service', 'Service')])
    sale_price = fields.Float(string='Product Sale Price', default='1.00', help='Sale Price of the proudct')
    cost_price = fields.Float(string='Product Cost Price', default='1.00', help='Cost Price of the proudct')

    category_id = fields.Many2one(comodel_name='product.category.ept', string='Product Category id',
                                  help='Product Category id')
    uom_id = fields.Many2one(comodel_name='product.uom.ept', string='Product UOM id', help='Product Uom id')
    description = fields.Text(string='Product Description', help='Description of the product')

    product_stock = fields.Float(string='Product Stock', help='Stock  of the proudct', compute='_compute_product_stock',
                                 readonly=False)


    def _compute_volume(self):
        for product in self:
            product.volume=product.length*product.width
    def _compute_product_stock(self):
        inventorylocation = self.env.context.get('location')
        if self.env.context.get('location'):
            stock_location = inventorylocation.ids
        else:
            stock_location = self.env['stock.warehouse.ept'].search([]).stock_location_id.ids

        for products in self:
            purchase_qty_done = sum([productstock.qty_done for productstock in self.env['stock.move.ept'].search(
                [('destination_location_id', 'in', stock_location), ('state', '=', 'done'),
                 ('product_id', '=', products.id)])])

            delivery_qty_done = sum([productstock.qty_done for productstock in self.env['stock.move.ept'].search(
                [('source_location_id', 'in', stock_location), ('state', '=', 'done'),
                 ('product_id', '=', products.id)])])

            products.product_stock = purchase_qty_done - delivery_qty_done

    def open_action(self):
        action = self.env["ir.actions.act_window"]._for_xml_id('sale_ept.product_update_stock_action')
        return action