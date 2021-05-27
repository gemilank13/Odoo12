import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DJBCLaporanPosisi(models.TransientModel):
    _inherit='djbc.nofas.posisi.wizard'

    @api.multi
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select djbc_nofas_posisi(%s,%s)",(self.date_start, self.date_end))
        data = {
            'model': 'djbc.nofas.posisi.wizard',
            'form': self.read()[0]
        }
        
        return self.env.ref('ab_laporan_posisi.posisi_xlsx').report_action(self, data=data)


        


