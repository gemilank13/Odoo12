from odoo import models, fields, api

class InheritStockMove(models.Model):
    _inherit='stock.move'

    buyer = fields.Char(string="Buyer", compute="_get_value")
    style = fields.Char(string="Style", compute="_get_value2")
    no_po = fields.Char(string="Nomor PO", compute="_get_value3")

    @api.one
    @api.depends('reference')
    def _get_value(self):

        field1 = self.env ['stock.picking'].search([('name','=',self.reference)])
        self.buyer = field1.buyer.name or False

    @api.one
    @api.depends('reference')
    def _get_value2(self):

        field1 = self.env ['stock.picking'].search([('name','=',self.reference)])
        self.style = field1.style or False

    @api.one
    @api.depends('reference')
    def _get_value3(self):

        field1 = self.env ['stock.picking'].search([('name','=',self.reference)])
        self.no_po = field1.no_po or False