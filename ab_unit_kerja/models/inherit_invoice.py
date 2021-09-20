from odoo import models, fields, api

class InheritInvoice(models.Model):
    _inherit='account.invoice'

    unit_kerja = fields.Selection([ ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],string= 'Unit Kerja')
    ab_date= fields.Date(string="Date of Exportation/Production")
    ab_keterangan= fields.Char(string="Keterangan")

    @api.model
    def default_get(self, fields):
    	res = super(InheritInvoice, self).default_get(fields)
    	res.update({
    		'unit_kerja':self.env.user.unit_kerja or False,
    		})
    	return res

    # ab_unit_kerja= fields.Char(string="Unit Kerja", compute="_get_value")

    # @api.one
    # @api.depends('name')
    # def _get_value(self):
    #     field1 = self.env ['res.users'].search([('name','=',self.user_id.name)])
    #     self.ab_unit_kerja = field1.unit_kerja

    # ab_unit_kerja= fields.Char(string="Unit Kerja")

