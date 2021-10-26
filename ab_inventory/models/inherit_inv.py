from odoo import models, fields

class InheritInventory(models.Model):
    _inherit='stock.picking'

    buyer = fields.Many2one('res.partner','Buyer')
    style = fields.Char(string="Style")
    no_po = fields.Char(string="Nomor PO")
