# import logging

from odoo import models, fields, api
from datetime import datetime, timedelta

# _logger = logging.getLogger(__name__)

class PRBalanceSheetWizard(models.TransientModel):
    _name='pr.balance.sheet.wizard'

    date_start = fields.Date(string='Date Start',default=fields.Date.today()-timedelta(days=30))
    date_end = fields.Date(string='Date End', default=fields.Date.today())

    date_start2 = fields.Date(string='Date Start',default=fields.Date.today().strftime('%Y-01-01'))
    date_end2 = fields.Date(string='Date End',default=fields.Date.today())
    
    currency = fields.Many2one(comodel_name="res.currency", string="Currency", required=False, )
    is_manual_rate = fields.Boolean(string="Is Manual Rate?")
  
    rate = fields.Float(string='Rate', default=1)
    currency_date = fields.Date(string="Currency Date", default=fields.Date.today())

    unit_kerja = fields.Selection([ ('ALL', 'ALL'), ('BOB', 'BOB'),('ACW', 'ACW'), ('SOR', 'SOR'), ('CIG', 'CIG')],'Unit Kerja')
    type_laporan = fields.Selection([ ('COGNOS', 'COGNOS'),('PMP', 'PMP')],'Laporan', default="PMP")
    
     	
    def call_pr_balance_sheet(self):
        cr=self.env.cr
        # _logger.info(self.djbc_category_id.id)
        cr.execute("select pr_balance_sheet(%s,%s,%s,%s,%s)",(self.date_start, self.date_end, self.date_start2, self.date_end2, self.unit_kerja))
        waction = self.env.ref("pr_balance_sheet_v2.""pr_balance_sheet_action")
        result = waction.read()[0]
        return result
    
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select pr_balance_sheet(%s,%s,%s,%s,%s)",(self.date_start, self.date_end, self.date_start2, self.date_end2, self.unit_kerja))
        data = {
            'model': 'pr.balance.sheet.wizard',
            'form': self.read()[0]
        }
        return self.env.ref('pr_balance_sheet_v2.balance_sheet_xlsx').report_action(self, data=data)
    
    @api.onchange('date_end')
    def onchange_date(self):
        res={}
        if self.date_start>self.date_end:
            res = {'warning':{
                'title':('Warning'),
                'message':('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')}}
        if res:
            return res
    
    @api.onchange('date_start')
    def onchange_date_start(self):
        self.date_end=self.date_start + timedelta(days=30)
        # self.date_start2=self.date_start + timedelta(days=30)
        # self.date_end2=self.date_start2 + timedelta(days=30)
        return


        


