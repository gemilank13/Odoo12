from odoo import models, fields, api

class InheritJournalItem(models.Model):
    _inherit='account.move.line'

    unit_kerja = fields.Selection([ ('ALL', 'ALL'), ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
