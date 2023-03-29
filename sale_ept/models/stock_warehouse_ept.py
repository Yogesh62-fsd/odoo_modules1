from odoo import models,fields,api

class StockWarehouseEpt(models.Model):
    _name='stock.warehouse.ept'
    _description='Stock Warehouse Ept'

    name=fields.Char(string='Warehouse Name',help='Name of the warehouse')
    short_code=fields.Char(string='Warehouse Code',help='Short Code of the warehouse')
    address_id=fields.Many2one(comodel_name='res.partner.ept',string='Warehouse Address',help='Address of the warehouse')
    stock_location_id=fields.Many2one(comodel_name='stock.location.ept',string='Stock Location',help='Stock Location of the warehouse')
    view_location_id=fields.Many2one(comodel_name='stock.location.ept',string='View Location',help=' View Location of the warehouse')

    @api.model
    def create(self,vals):
        location=self.env['stock.location.ept']

        stocklocation_view=location.create({'name':vals['name']+'View','location_type':'View','is_scrap_location':True})
        stocklocation_internal= location.create({'name':vals['name']+'Internal','location_type':'Internal','parent_id':stocklocation_view.id,'is_scrap_location':True}) #creating the record for stock location internal and view type

        vals['stock_location_id']=stocklocation_internal.id
        vals['view_location_id']=stocklocation_view.id
        print(self.stock_location_id)
        return  super(StockWarehouseEpt,self).create(vals)


