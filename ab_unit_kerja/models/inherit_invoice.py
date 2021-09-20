from odoo import models, fields, api

class InheritInvoice(models.Model):
    _inherit='account.invoice'

    unit_kerja = fields.Selection([ ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
    ab_date= fields.Date(string="Date of Exportation/Production")
    ab_keterangan= fields.Char(string="Keterangan")
    
