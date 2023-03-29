from odoo import models,fields,api

class CrmLeadLineEpt(models.Model):
    _name='crm.lead.line.ept'
    _description='Crm Lead Line Ept'

    product_id=fields.Many2one(comodel_name='product.ept',string='Lead Line Product',help='Product of the Lead Line')
    name=fields.Char(string='Description',help='Description of the lead line product')
    expected_sell_qty =fields.Float(string='Expected Sell Qty',help='Expected sell quantity of the lead line product')
    uom_id=fields.Many2one(comodel_name='product.uom.ept',string='Lead Line Uom Id',help='UOm id of Lead line')
    lead_id=fields.Many2one(comodel_name='crm.lead.ept',string='Lead id ',help='Lead id of the lead line ept')

    @api.onchange('product_id')
    def onchange_name(self):
       self.name=self.product_id.description
       self.uom_id=self.product_id.uom_id