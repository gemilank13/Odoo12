from odoo import models, fields, api


class DJBCNofasMasukWiz(models.TransientModel):
    _name = "djbc.nofas.masuk.wizard.v4"
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')

    @api.multi
    def generate_laporan(self):
        cr = self.env.cr
        cr.execute("select djbc_nofas_masuk_v4(%s,%s)",(self.date_start, self.date_end))
        waction = self.env.ref("ab_nofas_masuk_v4.""nofas_masuk_action")
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

    @api.multi
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select djbc_nofas_masuk_v4(%s,%s)",(self.date_start, self.date_end))
        data = {
            'model': 'djbc.nofas.masuk.wizard.v4',
            'form': self.read()[0]
        }
        
        return self.env.ref('ab_nofas_masuk_v4.nofas_masuk_xlsx').report_action(self, data=data)
