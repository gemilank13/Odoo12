from odoo import models, fields

class DJBCStockLocation(models.Model):
    _inherit='stock.location'

    is_waste_kite = fields.Boolean(string="Is a Waste Kite?",  )
