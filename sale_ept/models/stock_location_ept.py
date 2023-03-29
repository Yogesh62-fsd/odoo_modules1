from odoo import models,fields

class StockLocationEpt(models.Model):
    _name='stock.location.ept'
    _descripiton='Stock Location Ept'

    name=fields.Char(string=' Stock Location Name',help='Name of the Stock location')
    parent_id=fields.Many2one(comodel_name='stock.location.ept',string=' Stock Parent Location ',help='Parent Id of the Stock location')
    location_type=fields.Selection(string='Stock Location Type',selection=[('Vendor','Vendor'),('Customer','Customer'),('Internal','Internal'),('Inventory Loss','Inventory Loss'),('Production','Production'),('Transit','Transit'),('View','View')],help='Stock Location type ')
    is_scrap_location=fields.Boolean(string='ScarpLocation',default=False,help='Scarp Location')



