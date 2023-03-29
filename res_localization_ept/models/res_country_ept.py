from odoo import models, fields, api


class CountryEPT(models.Model):
    _name = "res.country.ept"
    _description = "Country EPT"

    name = fields.Char(string="Country Name ", help="Name of the Country")
    code = fields.Char(string="Country Code ", help="Code of the Country")
    state_ids = fields.One2many(comodel_name="res.state.ept", inverse_name="country_id", string="Country State Ids ",
                                help="Country State Ids of the Country", copy=True)

    _sql_constraints = [('country_code_unique', 'unique(code)', 'Warning: Country Code Must be unique....')]
    def get_details(self):
        # print(self.state_ids.city_ids.name)
        city_obj = self.env['res.country.ept'].search([]).state_ids.city_ids.mapped('name')
        print('cities = ', city_obj)

        # print(self.state_ids.name)

        # for state in self.state_ids:
        #     for cities in state.city_ids:
        #         print(cities.name)
        # for city in self.state_ids.city_ids:
        #     print('ciites is ',city.name)

        self.copy()

    @api.model
    def _name_search(self, name, args=None, operator='ilike',limit=None):
        print('Name Search is called ..............')
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        args = args + domain
        print(args, name)
        return self._search(args,limit=None)

