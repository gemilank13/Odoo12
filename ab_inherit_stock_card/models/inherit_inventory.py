from odoo import models, fields, api

class InheritInventory(models.Model):
    _inherit='stock.picking'

    ab_project = fields.Char(string="Project", compute='_get_value')

    @api.model
    def _get_value(self):
        for rec in self:
            field1 = self.env ['mrp.production'].search([('picking_ids','=',rec.id)])
            rec.ab_project = field1.ab_project
            return
    	# field1 = self.env['mrp.production'].search([])
    	# field1.ab_project = self.ab_project
    	# return



    # @api.model
    # def create(self, vals):
    #     field1 = self.env['mrp.production'].search([('field1', '=', 'Some Value')], limit=1).field1
    #     vals.update({'field2': field1})
    #     return super(MyClass2, self).create(vals)