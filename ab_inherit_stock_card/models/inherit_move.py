from odoo import models, fields, api

class InheritStockMove(models.Model):
    _inherit='stock.move'

    @api.one
    @api.depends('name')
    def _get_value(self):
        field1 = self.env ['mrp.production'].search([('name','=',self.origin)])
        self.ab_project = field1.ab_project

    ab_project = fields.Char(string="Project", store=True, readonly=False, compute='_get_value')
