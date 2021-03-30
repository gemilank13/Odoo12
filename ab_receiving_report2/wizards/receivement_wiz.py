import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ReceivementWizard(models.TransientModel):
    _name='receivement.wizard'

    # person = fields.Many2one('res.users', string="Person")
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')

    @api.multi
    def generate_laporan_xls(self):
        # cr=self.env.cr
        # cr.execute("select stock_picking(%s,%s)",(self.date_start, self.date_end))
        data = {
            'model': 'receivement.wizard',
            'form': self.read()[0]
        }
        
        return self.env.ref('ab_receiving_report2.receivement_xlsx').report_action(self, data=data)

