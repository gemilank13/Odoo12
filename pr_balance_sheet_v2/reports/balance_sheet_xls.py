import logging
from odoo import models
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class BalanceSheetXlsx(models.AbstractModel):
    _name = 'report.balance_sheet_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        
        if data['form']['is_manual_rate']:
            this_rate=data['form']['rate']
        else:
            id_idr=self.env['res.currency'].search([('name', '=', 'IDR')])
            id_foreign=self.env['res.currency'].search([('name', '=', data['form']['currency'])])
            rate_foreign=self.env['res.currency.rate'].search([('currency_id', '=', id_foreign.id),
            ('name','<',data['form']['currency_date'])],limit=1).rate
            rate_idr=self.env['res.currency.rate'].search([('currency_id', '=', id_idr.id),
            ('name','<',data['form']['currency_date'])],limit=1).rate
            
            this_rate=rate_idr*rate_foreign

        # _logger.info("------>" + str(this_rate))
        sheet2 = workbook.add_worksheet('Profit and Loss')
        
        sheet2.set_column(0,0,10)
        sheet2.set_column(1,1,30)
        sheet2.set_column(2,2,15)
        sheet2.set_column(3,3,15)

        format0 = workbook.add_format()
        format0.set_font_size(10)
        format0.set_bold()

        
        format1 = workbook.add_format()
        format1.set_font_size(10)
        format1.set_bold()
        format1.set_border()

        format2 = workbook.add_format()
        format2.set_font_size(10)
        # format2.set_indent(1)

        money = workbook.add_format({'num_format': '#,##0.00'})
        money.set_font_size(10)
        # money = workbook.add_format({'num_format': '($#,##0_);($#,##0)'})

        formatcode = workbook.add_format({
            'align':'right',
            'font_size': 10,
            })
        # string = "freeCodeCamp"
        # print(string[0:5])
        # freeC
        # 2020-08-01
        # 0123456789
        y_start = data['form']['date_start'][0:4]
        m_start = data['form']['date_start'][5:7]
        d_start = data['form']['date_start'][8:10]
        y_end = data['form']['date_end'][0:4]
        m_end = data['form']['date_end'][5:7]
        d_end = data['form']['date_end'][8:10]
        y_start2 = data['form']['date_start2'][0:4]
        m_start2 = data['form']['date_start2'][5:7]
        d_start2 = data['form']['date_start2'][8:10]
        y_end2 = data['form']['date_end2'][0:4]
        m_end2 = data['form']['date_end2'][5:7]
        d_end2 = data['form']['date_end2'][8:10]
        # raise UserError(_("You should provide a lot/serial number for a component"))


        # sheet2.write(0, 0, 'Laba Rugi', format0)
        # sheet2.write(1, 0, 'Current Period: ' + d_start+'-'+m_start+'-'+y_start + ' s.d. ' + d_end+'-'+m_end+'-'+y_end, format0)
        # sheet2.write(2, 0, 'Previous Period: ' + d_start2+'-'+m_start2+'-'+y_start2 + ' s.d. ' + d_end2+'-'+m_end2+'-'+y_end2, format0)
        # sheet2.write(3, 0, 'Currency: ' + str(data['form']['currency']), format0)
        # sheet2.write(4, 0, 'Rate: ' + str(this_rate), format0)
        # sheet2.write(6, 0, 'Code', format1)
        # sheet2.write(6, 1, 'Account Name', format1)
        # sheet2.write(6, 2, 'Current Period', format1)
        # sheet2.write(6, 3, 'Previous Period', format1)
        # sheet2.write(2, 4, 'Currency', format1)
        # sheet2.write(2, 5, 'Original Current Period', format1)
        # sheet2.write(2, 6, 'Original Previous Period', format1)

        sheet2.write(0, 0, 'PT PENYELESAIAN MASALAH PROPERTY', format0)
        sheet2.write(1, 0, 'INCOME STATEMENT', format0)
        # sheet2.write(2, 0, '', format0)

        sheet2.write(4, 0, ' ', format1)
        sheet2.write(4, 1, ' ', format1)
        sheet2.write(4, 2, 'Current Period', format1)
        sheet2.write(4, 3, 'Year to Date', format1)

        tot_cur_period_pendapatan = 0
        tot_prev_period_pendapatan = 0

        i = 5
        # sheet2.write(i, 0, "Pendapatan", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Income')])
        # for obj in lines:
        #     if obj.cur_period==0 and obj.prev_period==0:
        #         continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, format2)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, (obj.cur_period * -1)/this_rate, money)
        #     sheet2.write(i, 3, (obj.prev_period * -1)/this_rate, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_pendapatan = tot_cur_period_pendapatan + (obj.cur_period / this_rate)
        #     tot_prev_period_pendapatan = tot_prev_period_pendapatan + ( obj.prev_period / this_rate)
        # i = i + 1
        # sheet2.write(i, 0, 'Total Pendapatan', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # tot_cur_period_pendapatan = tot_cur_period_pendapatan * -1
        # tot_prev_period_pendapatan = tot_prev_period_pendapatan * -1
        # sheet2.write(i, 2, tot_cur_period_pendapatan, money)
        # sheet2.write(i, 3, tot_prev_period_pendapatan, money)

        i = i + 1
        sheet2.write(i, 0, "Revenue", format0)
        tot_cur_period_hpp = 0
        tot_prev_period_hpp = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Revenue')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_hpp = tot_cur_period_hpp + (obj.cur_period)
            tot_prev_period_hpp = tot_prev_period_hpp + (obj.prev_period)

        i = i + 1
        sheet2.write(i, 0, 'Total Revenue', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, tot_cur_period_hpp * -1 , money)
        sheet2.write(i, 3, tot_prev_period_hpp * -1, money)

        i = i + 2
        sheet2.write(i, 0, "Cost of Production", format0)

        i = i + 1
        sheet2.write(i, 1, "Material Cost", format0)
        tot_cur_period_cost = 0
        tot_prev_period_cost = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Material Cost')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
            tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        i = i + 1
        sheet2.write(i, 1, "Direct Labor Cost", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Direct Labor Cost')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
            tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        i = i + 1
        sheet2.write(i, 1, "Indirect Labor Cost", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Indirect Labor Cost')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
            tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)

        i = i + 1
        sheet2.write(i, 1, "Transportation", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Transportation')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
            tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        i = i + 1
        sheet2.write(i, 1, "Energy Production", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Energy Production')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
            tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        i = i + 1
        sheet2.write(i, 1, "Maintenance", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Maintenance')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
            tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        i = i + 1
        sheet2.write(i, 1, "Other Overhead", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Overhead')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
            tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        i = i + 2
        sheet2.write(i, 0, 'Total Cost of Production', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, tot_cur_period_cost * -1, money)
        sheet2.write(i, 3, tot_prev_period_cost * -1, money)

        i = i + 2
        sheet2.write(i, 0, 'Gross Margin', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, (tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        sheet2.write(i, 3, (tot_prev_period_cost + tot_prev_period_hpp) * -1, money)


        i = i + 2
        sheet2.write(i, 0, "Operating Expenses", format0)
        tot_cur_period_exp = 0
        tot_prev_period_exp = 0

        i = i + 1
        sheet2.write(i, 1, "Admin Personel Expenses", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Admin Personel Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period , money)
            sheet2.write(i, 3, obj.prev_period, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
            tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        i = i + 1
        sheet2.write(i, 1, "Facility Expenses", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Facility Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period , money)
            sheet2.write(i, 3, obj.prev_period, money)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
            tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        i = i + 1
        sheet2.write(i, 1, "Vehicle Expenses", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Vehicle Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period , money)
            sheet2.write(i, 3, obj.prev_period, money)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
            tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        i = i + 1
        sheet2.write(i, 1, "IT Expenses", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'IT Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period , money)
            sheet2.write(i, 3, obj.prev_period, money)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
            tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        i = i + 1
        sheet2.write(i, 1, "General Admin Expenses", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'General Admin Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period , money)
            sheet2.write(i, 3, obj.prev_period, money)
            tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
            tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        i = i + 2
        sheet2.write(i, 0, 'Total Operating Expenses', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, tot_cur_period_exp, money)
        sheet2.write(i, 3, tot_prev_period_exp, money)

        i = i + 2
        sheet2.write(i, 0, 'EBITDA', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        sheet2.write(i, 3, (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)


        i = i + 2
        sheet2.write(i, 0, "Depreciation", format0)
        tot_cur_period_dep = 0
        tot_prev_period_dep = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Depreciation')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
            tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)

        i = i + 1
        sheet2.write(i, 0, "Amortization", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Amortization')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
            tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)

        i = i + 2
        sheet2.write(i, 0, 'Total Depreciation and Amort.', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, tot_cur_period_dep * -1, money)
        sheet2.write(i, 3, tot_prev_period_dep * -1, money)

        i = i + 2
        sheet2.write(i, 0, 'EBIT', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        sheet2.write(i, 3, (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)

        i = i + 2
        sheet2.write(i, 0, "Other Income/ Expenses", format0)
        tot_cur_other_ie = 0
        tot_prev_other_ie = 0

        i = i + 1
        sheet2.write(i, 1, "Other Income", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Interest Income')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Profits on Currency Exchange')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non Operating Income')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Extraordinary Income')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)


        i = i + 1
        sheet2.write(i, 1, "Other Expenses", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Interest Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Loss on Currency Exchange')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non Operating Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)


        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Extraordinary Expenses')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, money)
            sheet2.write(i, 3, obj.prev_period * -1, money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
            tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)


        i = i + 2
        sheet2.write(i, 0, 'Total Other Income/ Expenses', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, tot_cur_other_ie * -1, money)
        sheet2.write(i, 3, tot_prev_other_ie * -1, money)

        i = i + 2
        sheet2.write(i, 0, 'Net Income/(loss)', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)


        i = i + 2
        sheet2.write(i, 0, "Taxes", format0)
        tot_cur_tax = 0
        tot_prev_tax = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Taxes')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            tot_cur_tax = tot_cur_tax + (obj.cur_period)
            tot_prev_tax = tot_prev_tax + (obj.prev_period)

            sheet2.write(i, 0, obj.code, formatcode)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_tax , money)
            sheet2.write(i, 3, tot_prev_tax , money)
            # sheet2.write(i, 4, obj.currency, format2)
            # sheet2.write(i, 5, obj.ori_cur_period, money)
            # sheet2.write(i, 6, obj.ori_prev_period, money)
            

        i = i + 2
        sheet2.write(i, 0, 'EAT', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)

        e_a_t = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
        e_a_t2= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
        # i = i + 2
        # sheet2.write(i, 0, 'Laba Kotor', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # laba_kotor_cur_period = tot_cur_period_pendapatan-tot_cur_period_hpp
        # laba_kotor_prev_period = tot_prev_period_pendapatan-tot_prev_period_hpp
        # sheet2.write(i, 1, laba_kotor_cur_period , money)
        # sheet2.write(i, 2, laba_kotor_prev_period, money)

        # i = i + 2
        # sheet2.write(i, 0, "Beban Adm dan Umum", format0)
        # tot_cur_period_exp = 0
        # tot_prev_period_exp = 0
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Expenses')])
        # for obj in lines:
        #     if obj.cur_period==0 and obj.prev_period==0:
        #         continue
        #     i = i + 1
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period, money)
        #     sheet2.write(i, 3, obj.prev_period, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
        #     tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        # i = i + 1
        # sheet2.write(i, 0, 'Beban Adm dam Umum', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, tot_cur_period_exp, money)
        # sheet2.write(i, 3, tot_prev_period_exp, money)

        # i = i + 2
        # sheet2.write(i, 0, "Pendapatan Lain-lain", format0)
        # tot_cur_period_oti = 0
        # tot_prev_period_oti = 0
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Income')])
        # for obj in lines:
        #     if obj.cur_period==0 and obj.prev_period==0:
        #         continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, format2)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1 /this_rate, money)
        #     sheet2.write(i, 3, obj.prev_period * -1 /this_rate, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_oti = tot_cur_period_oti + (obj.cur_period/this_rate)
        #     tot_prev_period_oti = tot_prev_period_oti + (obj.prev_period/this_rate)
        # i = i + 1
        # sheet2.write(i, 0, 'Pendapatan Lain-lain', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # tot_cur_period_oti = tot_cur_period_oti * -1
        # tot_prev_period_oti = tot_prev_period_oti * -1
        # sheet2.write(i, 2, tot_cur_period_oti, money)
        # sheet2.write(i, 3, tot_prev_period_oti, money)

        # i = i + 2
        # sheet2.write(i, 0, 'Laba Bersih', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # laba_bersih_cur_period = laba_kotor_cur_period - tot_cur_period_exp + tot_cur_period_oti
        # laba_bersih_prev_period = laba_kotor_prev_period - tot_prev_period_exp + tot_prev_period_oti
        # sheet2.write(i, 2, laba_bersih_cur_period, money)
        # sheet2.write(i, 3, laba_bersih_prev_period, money)


        sheet = workbook.add_worksheet('Balance Sheet')
        sheet.set_column(0, 0, 10)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)

        

        sheet.write(0, 0, 'PT. PENYELESAIAN MASALAH PROPERTY', format1)
        sheet.write(1, 0, 'STATEMENT OF FINANCIAL POSITION', format1)
        sheet.write(2, 0, '', format1)

        sheet.write(4,0,'',format1)
        sheet.write(4,1,'',format1)
        sheet.write(4,2,'Current Period',format1)
        sheet.write(4,3,'Year to Date',format1)
        tot_cur_period = 0
        tot_prev_period = 0
        tot_ori_cur_period = 0
        tot_ori_prev_period = 0
        tot_non_cur_period = 0
        tot_non_prev_period = 0


        i=6
        sheet.write(i, 0, "Asset", format0)
        i = i + 1
        sheet.write(i, 0, "Current Assets", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Current Assets')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Cash & Cash equivalents", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type','=','Cash & Cash equivalents')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Receivable", format0)
        lines = self.env['pr.balance_sheet'].search([('code', '>=', '112000'),('code', '<', '113000')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Other Receivable", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Receivable')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Prepayments", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Prepayments')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Prepaid Tax", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Prepaid Tax')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Inventory Stock Material", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Inventory Stock Material')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Inventory Semi Finished Goods", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Inventory Semi Finished Goods')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Inventory Sparepart", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Inventory Sparepart')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Other Current Assets", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Current Assets')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)

        i=i+2
        sheet.write(i, 0,'Total Current Assets', format0)
        sheet.write(i, 2, tot_cur_period, money)
        sheet.write(i, 3, tot_prev_period, money)


        i = i + 2
        sheet.write(i, 0, "Non-Current Assets", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non-Current Assets')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Fixed Assets Acquisition", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Fixed Assets Acquisition')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Accumulation Depreciation", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Accumulation Depreciation')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Intangible Assets", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Intangible Assets')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)

        
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Fixed Assets Land')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)

        lines = self.env['pr.balance_sheet'].search([('code', '=', '124001')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Other Non Current Assets", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Non Current Assets')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)

        i=i+2
        sheet.write(i, 0,'Total Non Current Assets', format0)
        sheet.write(i, 2, tot_non_cur_period, money)
        sheet.write(i, 3, tot_non_prev_period, money)

        i=i+2
        sheet.write(i, 0,'Total Assets', format0)
        sheet.write(i, 2, (tot_cur_period+tot_non_cur_period), money)
        sheet.write(i, 3, (tot_prev_period+tot_non_prev_period), money)



        i = i + 3
        sheet.write(i, 0, "Liabilities and Equity", format0)
        tot_cur_period_hutang = 0
        tot_prev_period_hutang = 0
        tot_non_cur_period_hutang = 0
        tot_non_prev_period_hutang = 0

        i = i + 1
        sheet.write(i, 0, "Current Liabilities", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Current Liabilities')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)


        i = i + 1
        sheet.write(i, 1, "Payable", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Payable')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)


        i = i + 1
        sheet.write(i, 1, "Other Payable", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Payable')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Tax Payable", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Tax Payable')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Accruals And Deferred Income", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Accruals And Deferred Income')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "S/T Loans", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'S/T Loans')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "S/T Provision", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'S/T Provision')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)

        i = i + 2
        sheet.write(i, 0, 'Total Current Liabilities', format0)
        # sheet.write(i, 1, obj.name, format2) 
        sheet.write(i, 2, tot_cur_period_hutang * -1, money)
        sheet.write(i, 3, tot_prev_period_hutang * -1, money)


        i = i + 2
        sheet.write(i, 0, "Non-Current Liabilities", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non-Current Liabilities')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_non_cur_period_hutang = tot_non_cur_period_hutang + (obj.cur_period)
            tot_non_prev_period_hutang = tot_non_prev_period_hutang + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "L/T Loans", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'L/T Loans')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_non_cur_period_hutang = tot_non_cur_period_hutang + (obj.cur_period)
            tot_non_prev_period_hutang = tot_non_prev_period_hutang + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "L/T Provision", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'L/T Provision')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_non_cur_period_hutang = tot_non_cur_period_hutang + (obj.cur_period)
            tot_non_prev_period_hutang = tot_non_prev_period_hutang + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Other Non Current Liabilities", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Non Current Liabilities')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_non_cur_period_hutang = tot_non_cur_period_hutang + (obj.cur_period)
            tot_non_prev_period_hutang = tot_non_prev_period_hutang + (obj.prev_period)

        i = i + 2
        sheet.write(i, 0, 'Total Non-Current Liabilities', format0)
        # sheet.write(i, 1, obj.name, format2) 
        sheet.write(i, 2, (tot_non_cur_period_hutang * -1), money)
        sheet.write(i, 3, (tot_non_prev_period_hutang * -1), money)

        i = i + 2
        sheet.write(i, 0, "Equity", format0)
        tot_cur_period_modal =  0
        tot_prev_period_modal =  0
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Current Year Earnings')])
        # for obj in lines:
        #     i = i + 1
        #     # sheet.write(i, 0, obj.code, format2)
        #     sheet.write(i, 0, obj.name, format2)
        #     sheet.write(i, 1, laba_bersih_cur_period, money)
        #     sheet.write(i, 2, laba_bersih_prev_period, money)
        #     tot_cur_period_modal = tot_cur_period_modal + (laba_bersih_cur_period * -1) # obj.cur_period
        #     tot_prev_period_modal = tot_prev_period_modal + (laba_bersih_prev_period * -1)  # obj.prev_period
        # i=i+1
        # sheet.write(i, 2, laba_bersih_cur_period, money)
        # sheet.write(i, 3, laba_bersih_prev_period, money)

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Equity')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Share & Capital Reserves", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Share & Capital Reserve')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            # sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Dividend", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Dividend')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Profit/Loss Carried Forward", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Profit/Loss Carried Forward')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)


        i = i + 1
        sheet.write(i, 1, "Profit/Loss Of Period", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Profit/Loss Of Period')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, e_a_t, money)
            sheet.write(i, 3, e_a_t2, money)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)

        i = i + 1
        sheet.write(i, 1, "Other Equity Component", format0)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Equity Component')])
        for obj in lines:
            # if obj.cur_period==0 and obj.prev_period==0:
            #     continue
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)

        i = i + 2
        sheet.write(i, 0, 'Total Equity', format0)
        # sheet.write(i, 1, obj.name, format2)
        sheet.write(i, 2, (tot_cur_period_modal + e_a_t) * -1, money)
        sheet.write(i, 3, (tot_prev_period_modal + e_a_t2)* -1, money)

        i = i + 2
        sheet.write(i, 0, 'Total Liabilities and Equity', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet.write(i, 1, (tot_cur_period_modal+tot_cur_period_hutang-tot_non_cur_period_hutang) * -1, money)
        # sheet.write(i, 2, (tot_prev_period_modal+tot_prev_period_hutang-tot_non_prev_period_hutang) * -1, money)

        sheet.write(i, 2, (tot_non_cur_period_hutang+tot_cur_period_hutang+tot_cur_period_modal-e_a_t) * -1, money)
        sheet.write(i, 3, (tot_non_prev_period_hutang+tot_prev_period_hutang+tot_prev_period_modal-e_a_t2) * -1, money)


        # sheet.write(6,0,'Account Code',format1)
        # sheet.write(6,1,'Account Name',format1)
        # sheet.write(6,2,'Current Period',format1)
        # sheet.write(6,3,'Previous Period',format1)
        # sheet.write(2,4,'Currency',format1)
        # sheet.write(2,5,'Original Current Period',format1)
        # sheet.write(2,6,'Original Previous Period',format1)

        # search account type = Bank and Cash
        # tot_cur_period = 0
        # tot_prev_period = 0
        # tot_ori_cur_period = 0
        # tot_ori_prev_period = 0

        # i=6
        # sheet.write(i, 0, "Asset", format0)
        # # i=i+1
        # # sheet.write(i, 0, "Kas dan Setara Kas", format0)
        # # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Bank and Cash')])
        # # for obj in lines:
        # #     if obj.cur_period==0 and obj.prev_period==0:
        # #         continue
        # #     i=i+1
        # #     # sheet.write(i,0,obj.code,format2)
        # #     sheet.write(i,0,obj.name,format2)
        # #     sheet.write(i,1,obj.cur_period/this_rate,money)
        # #     sheet.write(i,2,obj.prev_period/this_rate,money)
        # #     # sheet.write(i,4,obj.currency,format2)
        # #     # sheet.write(i,5,obj.ori_cur_period,money)
        # #     # sheet.write(i,6,obj.ori_prev_period,money)
        # #     tot_cur_period = tot_cur_period + obj.cur_period/this_rate
        # #     tot_prev_period = tot_prev_period + obj.prev_period/this_rate
        # #     # tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
        # #     # tot_ori_prev_period = tot_ori_prev_period + obj.prev_period
        # #     # raise UserError("yes working...6")

        # i = i + 1
        # sheet.write(i, 0, "Current Assets", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Current Assets')])
        # for obj in lines:
        #     if obj.cur_period==0 and obj.prev_period==0:
        #         continue
        #     i = i + 1
        #     # sheet.write(i, 0, obj.code, format2)
        #     sheet.write(i, 0, obj.name, format2)
        #     sheet.write(i, 1, obj.cur_period, money)
        #     sheet.write(i, 2, obj.prev_period, money)
        #     # sheet.write(i, 4, obj.currency, format2)
        #     # sheet.write(i, 5, obj.ori_cur_period, money)
        #     # sheet.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period = tot_cur_period + (obj.cur_period)
        #     tot_prev_period = tot_prev_period + (obj.prev_period)
        #     # tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
        #     # tot_ori_prev_period = tot_ori_prev_period + obj.prev_period

        

        # i = i + 1
        # sheet.write(i, 0, "Prepayments", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Prepayments')])
        # for obj in lines:
        #     if obj.cur_period==0 and obj.prev_period==0:
        #         continue
        #     i = i + 1
        #     # sheet.write(i, 0, obj.code, format2)
        #     sheet.write(i, 0, obj.name, format2)
        #     sheet.write(i, 1, obj.cur_period, money)
        #     sheet.write(i, 2, obj.prev_period, money)
        #     # sheet.write(i, 4, obj.currency, format2)
        #     # sheet.write(i, 5, obj.ori_cur_period, money)
        #     # sheet.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period = tot_cur_period + (obj.cur_period)
        #     tot_prev_period = tot_prev_period + (obj.prev_period)
        #     # tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
        #     # tot_ori_prev_period = tot_ori_prev_period + obj.prev_period

        # i=i+1
        # sheet.write(i, 0,'Total Current Assets', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet.write(i, 1, tot_cur_period, money)
        # sheet.write(i, 2, tot_prev_period, money)
        # # sheet.write(i, 4, obj.currency, format2)
        # # sheet.write(i, 5, obj.ori_cur_period, format2)
        # # sheet.write(i, 6, obj.ori_prev_period, format2)

        