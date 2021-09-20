from odoo import models, fields, api

class InheritUser(models.Model):
    _inherit='res.users'

    unit_kerja = fields.Selection([ ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
