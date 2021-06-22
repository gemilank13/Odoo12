from odoo import models, fields, api

class InheritInvoice(models.Model):
    _inherit='account.invoice'

    feeder_vessel = fields.Char(string="Feeder Vessel")
    place_receipt = fields.Char(string="Pleace of Receipt")
    ocean_vessel = fields.Char(string="Ocean Vessel")
    port_loading = fields.Char(string="Port of Loading")
    place_receipt = fields.Char(string="Pleace of Receipt")
    port_discharge = fields.Char(string="Port of Discharge")
    final_destination = fields.Char(string="Final Destination")
    hts_code = fields.Char(string="HTS Code")
    ship = fields.Char(string="Ship To")
    ship2 = fields.Char(string="Ship To")
    ship3 = fields.Char(string="Ship To")