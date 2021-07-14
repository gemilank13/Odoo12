import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DJBCKitePenghpInherit(models.TransientModel):
    _inherit='djbc.kite.penghp.wizard'

    @api.multi
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select djbc_kite_penghp(%s,%s)",(self.date_start, self.date_end))
        data = {
            'model': 'djbc.kite.penghp.wizard',
            'form': self.read()[0]
        }
        
        return self.env.ref('ab_djbc_kite_xls.kite_penghp_xlsx').report_action(self, data=data)


        


