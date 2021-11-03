from odoo import models, fields, api

class InheritInvoiceLine(models.Model):
    _inherit='account.invoice.line'

    unit_kerja = fields.Selection([ ('ALL', 'ALL'), ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
