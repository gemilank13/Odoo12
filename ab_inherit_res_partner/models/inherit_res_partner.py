from odoo import models, fields, api

class InheritResPartner(models.Model):
    _inherit='res.partner'

    is_subkontraktor =  fields.Boolean(string = "Sub Kontraktor")	