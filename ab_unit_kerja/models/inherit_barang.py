from odoo import models, fields, api

class InheritProduct(models.Model):
    _inherit='product.template'

    unit_kerja = fields.Selection([ ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
