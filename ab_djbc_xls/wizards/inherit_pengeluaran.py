import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DJBCPengeluaranWizardInherit(models.TransientModel):
    _inherit='djbc.nofas.keluar.v2.wizard'

    @api.multi
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select djbc_nofas_keluar_v2(%s,%s)",(self.date_start, self.date_end))
        data = {
            'model': 'djbc.nofas.keluar.v2.wizard',
            'form': self.read()[0]
        }
        
        return self.env.ref('ab_djbc_xls.pengeluaran_xlsx').report_action(self, data=data)


        


