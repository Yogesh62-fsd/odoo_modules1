from odoo import models,fields

class StockPickingExt(models.Model):
    _inherit='stock.picking'


    def create(self,vals):
        return  super(StockPickingExt,self).create(vals)