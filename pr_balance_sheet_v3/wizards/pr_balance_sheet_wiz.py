# import logging

from odoo import models, fields, api
from datetime import datetime, timedelta

# _logger = logging.getLogger(__name__)

class PRBalanceSheetWizard(models.TransientModel):
    _name='pr.balance.sheet.wizard_v3'

    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')

    date_start2 = fields.Date(string='Date Start')
    date_end2 = fields.Date(string='Date End')

    date_start3 = fields.Date(string='Date Start')
    date_end3 = fields.Date(string='Date End')
    
    currency = fields.Many2one(comodel_name="res.currency", string="Currency", required=False, )
    is_manual_rate = fields.Boolean(string="Is Manual Rate?")
  
    rate = fields.Float(string='Rate', default=1)
    currency_date = fields.Date(string="Currency Date", default=fields.Date.today())

    quarter = fields.Selection([('q1', 'Q1'),('q2', 'Q2'),('q3', 'Q3'),('q4', 'Q4')],'Quarter', default='q1')
    tahun = fields.Char(string='Tahun', default='2021')
    
     	
    def call_pr_balance_sheet(self):
        cr=self.env.cr
        # _logger.info(self.djbc_category_id.id)
        cr.execute("select pr_balance_sheet_v3(%s,%s,%s,%s,%s,%s)",(self.date_start, self.date_end, self.date_start2, self.date_end2, self.date_start3, self.date_end3))
        waction = self.env.ref("pr_balance_sheet_v3.""pr_balance_sheet_action")
        result = waction.read()[0]
        return result
    
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select pr_balance_sheet_v3(%s,%s,%s,%s,%s,%s)",(self.date_start, self.date_end, self.date_start2, self.date_end2, self.date_start3, self.date_end3))
        data = {
            'model': 'pr.balance.sheet.wizard_v3',
            'form': self.read()[0]
        }
        return self.env.ref('pr_balance_sheet_v3.balance_sheet_xlsx_v3').report_action(self, data=data)
    

    
    @api.onchange('quarter')
    def onchange_date_start(self):
        if self.quarter == 'q1' and self.tahun == '2021':

            self.date_start='2021-01-01'
            self.date_start2='2021-02-01'
            self.date_end='2021-01-31'
            self.date_end2='2021-02-28'

            self.date_start3='2021-03-01'
            self.date_end3='2021-03-31'

        if self.quarter == 'q1' and self.tahun == '2020':

            self.date_start='2020-01-01'
            self.date_start2='2020-02-01'
            self.date_end='2020-01-31'
            self.date_end2='2020-02-28'

            self.date_start3='2020-03-01'
            self.date_end3='2020-03-31'





        if self.quarter == 'q2' and self.tahun == '2021':

            self.date_start='2021-04-01'
            self.date_start2='2021-05-01'
            self.date_end='2021-04-30'
            self.date_end2='2021-05-31'

            self.date_start3='2021-06-01'
            self.date_end3='2021-06-30'

        if self.quarter == 'q2' and self.tahun == '2020':

            self.date_start='2020-04-01'
            self.date_start2='2020-05-01'
            self.date_end='2020-04-30'
            self.date_end2='2020-05-21'

            self.date_start3='2020-06-01'
            self.date_end3='2020-06-30'



        if self.quarter == 'q3' and self.tahun == '2021':

            self.date_start='2021-07-01'
            self.date_start2='2021-08-01'
            self.date_end='2021-07-31'
            self.date_end2='2021-08-31'

            self.date_start3='2021-09-01'
            self.date_end3='2021-09-30'

        if self.quarter == 'q3' and self.tahun == '2020':

            self.date_start='2020-07-01'
            self.date_start2='2020-08-01'
            self.date_end='2020-07-31'
            self.date_end2='2020-08-31'

            self.date_start3='2020-09-01'
            self.date_end3='2020-09-30'




        if self.quarter == 'q4' and self.tahun == '2021':

            self.date_start='2021-10-01'
            self.date_start2='2021-11-01'
            self.date_end='2021-10-31'
            self.date_end2='2021-11-30'

            self.date_start3='2021-12-01'
            self.date_end3='2021-12-31'

        if self.quarter == 'q4' and self.tahun == '2020':

            self.date_start='2020-10-01'
            self.date_start2='2020-11-01'
            self.date_end='2020-10-31'
            self.date_end2='2020-11-30'

            self.date_start3='2020-12-01'
            self.date_end3='2020-12-31'


            return


        


