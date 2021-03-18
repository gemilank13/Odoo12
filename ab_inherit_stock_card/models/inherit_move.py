from odoo import models, fields, api

class InheritStockMove(models.Model):
    _inherit='stock.move'

    ab_project = fields.Char(string="Project", compute='_get_value')

    @api.model
    def _get_value(self):
        for rec in self:
            field1 = self.env ['mrp.production'].search([('name','=',rec.origin)])
            rec.ab_project = field1.ab_project
            return