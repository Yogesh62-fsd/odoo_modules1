from odoo import models,fields

class CrmTeamEPT(models.Model):
    _name='crm.team.ept'
    _description='Crm Team Ept'

    name=fields.Char(string='Crm Team Name',help='Name of the crm Team ept')
    team_leader=fields.Many2one(comodel_name='res.users',string='CrmTeam Leader',help='Team leader of the crm lead ept')
