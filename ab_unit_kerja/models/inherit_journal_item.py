from odoo import models, fields, api

class InheritJournalItem(models.Model):
    _inherit='account.move.line'

    unit_kerja = fields.Selection([ ('ALL', 'ALL'), ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja',readonly=False, compute="_get_value2")


   	# @api.one
    # @api.depends('invoice_id')
    # def _get_value2(self):

    #     field1 = self.env['account.invoice'].search([('id','=',self.invoice_id)])
        	
    #     self.unit_kerja ='BOB'

    @api.one
    @api.depends('invoice_id.invoice_line_ids')
    def _get_value2(self):

        for line in self:
        	self.unit_kerja = line.invoice_id.invoice_line_ids.unit_kerja or False
        			