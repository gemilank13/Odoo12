from odoo import models, fields, api

class InheritJournal(models.Model):
    _inherit='account.move'

    @api.one
    @api.depends('name')
    def _get_value(self):
        field1 = self.env ['account.invoice'].search([('number','=',self.name)])
        self.unit_kerja = field1.unit_kerja


    # unit_kerja = fields.Selection([ ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
    unit_kerja = fields.Char(string="Unit Kerja", compute="_get_value")
