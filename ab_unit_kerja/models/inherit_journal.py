from odoo import models, fields, api

class InheritJournal(models.Model):
    _inherit='account.move'

    unit_kerja = fields.Selection([ ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja',readonly=False, compute="_get_value2")


    @api.one
    @api.depends('name')
    def _get_value2(self):

        field1 = self.env ['account.invoice'].search([('number','=',self.name)])
        self.unit_kerja = field1.unit_kerja or False


