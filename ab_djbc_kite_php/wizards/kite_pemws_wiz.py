from odoo import models, fields, api


class DJBCKitePemwsWiz(models.TransientModel):
    _name = "djbc.kite.pemws.wizard"
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')

    @api.multi
    def generate_laporan(self):
        cr = self.env.cr
        cr.execute("select djbc_kite_pemws(%s,%s)",(self.date_start, self.date_end))
        waction = self.env.ref("ab_djbc_kite_php.""kite_pemws_action")
        result = waction.read()[0]
        return result

    @api.onchange('date_end')
    @api.multi
    def onchange_date(self):
        res={}
        if self.date_start>self.date_end:
            res = {'warning':{
                'title':('Warning'),
                'message':('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')}}
        if res:
            return res
