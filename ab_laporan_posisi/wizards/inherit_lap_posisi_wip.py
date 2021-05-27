import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DJBCLaporanPosisiWIP(models.TransientModel):
    _inherit='djbc.posisi.wip.wizard'

    @api.multi
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select djbc_posisi_wip(%s,%s)",(self.date_start, self.date_end))
        data = {
            'model': 'djbc.posisi.wip.wizard',
            'form': self.read()[0]
        }
        
        return self.env.ref('ab_laporan_posisi.posisi_wip_xlsx').report_action(self, data=data)


        


