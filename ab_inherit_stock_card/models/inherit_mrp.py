from odoo import models, fields, api

class InheritMRP(models.Model):
    _inherit='mrp.production'

    ab_project = fields.Char(string="Project", store=True)	