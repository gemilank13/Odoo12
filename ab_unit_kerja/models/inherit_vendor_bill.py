from odoo import models, fields, api

class InheritVendorBill(models.Model):
    _inherit='account.invoice'

    unit_kerja = fields.Selection([ ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
