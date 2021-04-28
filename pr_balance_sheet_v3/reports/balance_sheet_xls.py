import logging
from odoo import models
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class BalanceSheetXlsx(models.AbstractModel):
    _name = 'report.balance_sheet_xlsx_v3'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        sheet2 = workbook.add_worksheet('Profit and Loss')
        
        sheet2.set_column(0,0,10)
        sheet2.set_column(1,1,30)
        sheet2.set_column(2,2,15)
        sheet2.set_column(3,3,15)
        sheet2.set_column(4,4,15)
        sheet2.set_column(5,5,15)

        format0 = workbook.add_format()
        format0.set_font_size(10)
        format0.set_bold()

        
        format1 = workbook.add_format()
        format1.set_font_size(10)
        format1.set_bold()
        format1.set_border()


        format3 = workbook.add_format()
        format3.set_font_size(10)
        format3.set_bold()
        format3.set_border()
        format3.set_bg_color('#808080')

        format2 = workbook.add_format()
        format2.set_font_size(10)
        # format2.set_indent(1)

        money = workbook.add_format({'num_format': '#,##0.00'})
        money.set_font_size(10)

        money2 = workbook.add_format({'num_format': '#,##0.00'})
        money2.set_font_size(10)
        money2.set_bg_color('#808080')
        # money = workbook.add_format({'num_format': '($#,##0_);($#,##0)'})

        formatcode = workbook.add_format({
            'align':'right',
            'font_size': 10,
            })

        # y_start = data['form']['date_start'][0:4]
        # m_start = data['form']['date_start'][5:7]
        # d_start = data['form']['date_start'][8:10]
        # y_end = data['form']['date_end'][0:4]
        # m_end = data['form']['date_end'][5:7]
        # d_end = data['form']['date_end'][8:10]
        # y_start2 = data['form']['date_start2'][0:4]
        # m_start2 = data['form']['date_start2'][5:7]
        # d_start2 = data['form']['date_start2'][8:10]
        # y_end2 = data['form']['date_end2'][0:4]
        # m_end2 = data['form']['date_end2'][5:7]
        # d_end2 = data['form']['date_end2'][8:10]
        quarter = data['form']['quarter']

        sheet2.write(0, 0, 'PT PENYELESAIAN MASALAH PROPERTY', format0)
        sheet2.write(1, 0, 'INCOME STATEMENT', format0)
        sheet2.write(2, 0, data['form']['tahun'], format0)


        ##########QUARTER 1

        if quarter == 'q1':
            sheet2.write(4, 0, ' ', format1)
            sheet2.write(4, 1, ' ', format1)
            sheet2.write(4, 2, 'Jan', format1)
            sheet2.write(4, 3, 'Feb', format1)
            sheet2.write(4, 4, 'Mar', format1)
            sheet2.write(4, 5, 'Q1', format3)

            i = 5

            i = i + 1
            sheet2.write(i, 0, "Revenue", format0)
            tot_cur_period_hpp = 0
            tot_prev_period_hpp = 0
            tot_last_period_hpp = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Revenue')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_hpp = tot_cur_period_hpp + (obj.cur_period)
                tot_prev_period_hpp = tot_prev_period_hpp + (obj.prev_period)
                tot_last_period_hpp = tot_last_period_hpp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, 'Total Revenue', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_hpp * -1 , money)
            sheet2.write(i, 3, tot_prev_period_hpp * -1, money)
            sheet2.write(i, 4, tot_last_period_hpp * -1, money)
            sheet2.write(i, 5, (tot_cur_period_hpp + tot_prev_period_hpp + tot_last_period_hpp) * -1, money2)

            i = i + 2
            sheet2.write(i, 0, "Cost of Production", format0)
            i = i + 1
            sheet2.write(i, 1, "Material Cost", format0)
            tot_cur_period_cost = 0
            tot_prev_period_cost = 0
            tot_last_period_cost = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Material Cost')])
            for obj in lines:
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Direct Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Direct Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Indirect Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Indirect Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Transportation", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Transportation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Energy Production", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Energy Production')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Maintenance", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Maintenance')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Other Overhead", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Overhead')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Cost of Production', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_cost * -1, money)
            sheet2.write(i, 3, tot_prev_period_cost * -1, money)
            sheet2.write(i, 4, tot_last_period_cost * -1, money)
            sheet2.write(i, 5, (tot_cur_period_cost+tot_prev_period_cost+tot_last_period_cost) * -1, money2)

            i = i + 2
            gross_cur = 0
            gross_prev = 0
            gross_last = 0
            sheet2.write(i, 0, 'Gross Margin', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_cost + tot_last_period_hpp) * -1, money)

            gross_cur = (tot_cur_period_cost + tot_cur_period_hpp) * -1
            gross_prev= (tot_prev_period_cost + tot_prev_period_hpp) * -1
            gross_last= (tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, gross_cur+gross_prev+gross_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Operating Expenses", format0)
            tot_cur_period_exp = 0
            tot_prev_period_exp = 0
            tot_last_period_exp = 0

            i = i + 1
            sheet2.write(i, 1, "Admin Personel Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Admin Personel Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Facility Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Facility Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Vehicle Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Vehicle Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "IT Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'IT Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "General Admin Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'General Admin Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Operating Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_exp, money)
            sheet2.write(i, 3, tot_prev_period_exp, money)
            sheet2.write(i, 4, tot_last_period_exp, money)
            sheet2.write(i, 5, tot_cur_period_exp+tot_prev_period_exp+tot_last_period_exp, money2)

            i = i + 2
            ebitda_cur=0
            ebitda_prev=0
            ebitda_last=0
            sheet2.write(i, 0, 'EBITDA', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)
            ebitda_cur = (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebitda_prev= (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebitda_last= (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, ebitda_cur+ebitda_prev+ebitda_last, money2)

            i = i + 2
            sheet2.write(i, 0, "Depreciation", format0)
            tot_cur_period_dep = 0
            tot_prev_period_dep = 0
            tot_last_period_dep = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Depreciation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, "Amortization", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Amortization')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Depreciation and Amort.', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_dep * -1, money)
            sheet2.write(i, 3, tot_prev_period_dep * -1, money)
            sheet2.write(i, 4, tot_last_period_dep * -1, money)
            sheet2.write(i, 5, (tot_cur_period_dep + tot_prev_period_dep + tot_last_period_dep) * -1, money2)

            i = i + 2
            ebit_cur = 0
            ebit_prev= 0
            ebit_last= 0
            sheet2.write(i, 0, 'EBIT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            ebit_cur = (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebit_prev= (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebit_last= (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, ebit_cur+ebit_prev+ebit_last, money2)


            i = i + 2
            sheet2.write(i, 0, "Other Income/ Expenses", format0)
            tot_cur_other_ie = 0
            tot_prev_other_ie = 0
            tot_last_other_ie = 0

            i = i + 1
            sheet2.write(i, 1, "Other Income", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Profits on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Other Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Loss on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)


            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Other Income/ Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_other_ie * -1, money)
            sheet2.write(i, 3, tot_prev_other_ie * -1, money)
            sheet2.write(i, 4, tot_last_other_ie * -1, money)
            sheet2.write(i, 5, (tot_cur_other_ie + tot_prev_other_ie + tot_last_other_ie) * -1, money2)

            i = i + 2
            net_cur=0
            net_prev=0
            net_last=0
            sheet2.write(i, 0, 'Net Income/(loss)', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            net_cur = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            net_prev= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            net_last= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, net_cur + net_prev + net_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Taxes", format0)
            tot_cur_tax = 0
            tot_prev_tax = 0
            tot_last_tax = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Taxes')])
            for obj in lines:
                i = i + 1
                tot_cur_tax = tot_cur_tax + (obj.cur_period)
                tot_prev_tax = tot_prev_tax + (obj.prev_period)
                tot_last_tax = tot_last_tax + (obj.last_period)

                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, tot_cur_tax , money)
                sheet2.write(i, 3, tot_prev_tax , money)
                sheet2.write(i, 4, tot_last_tax , money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

            i = i + 2
            tot_eat_cur=0
            tot_eat_prev=0
            tot_eat_last=0
            sheet2.write(i, 0, 'EAT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            tot_eat_cur= (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            tot_eat_prev=(tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            tot_eat_last=(tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp)* -1

            sheet2.write(i, 5, tot_eat_cur + tot_eat_prev + tot_eat_last, money2)

            e_a_t = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            e_a_t2= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            e_a_t3= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
        # i = i + 2
            


        ##########QUARTER 2

        if quarter == 'q2':
            sheet2.write(4, 0, ' ', format1)
            sheet2.write(4, 1, ' ', format1)
            sheet2.write(4, 2, 'Apr', format1)
            sheet2.write(4, 3, 'May', format1)
            sheet2.write(4, 4, 'Jun', format1)
            sheet2.write(4, 5, 'Q2', format1)

            i = 5

            i = i + 1
            sheet2.write(i, 0, "Revenue", format0)
            tot_cur_period_hpp = 0
            tot_prev_period_hpp = 0
            tot_last_period_hpp = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Revenue')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_hpp = tot_cur_period_hpp + (obj.cur_period)
                tot_prev_period_hpp = tot_prev_period_hpp + (obj.prev_period)
                tot_last_period_hpp = tot_last_period_hpp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, 'Total Revenue', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_hpp * -1 , money)
            sheet2.write(i, 3, tot_prev_period_hpp * -1, money)
            sheet2.write(i, 4, tot_last_period_hpp * -1, money)
            sheet2.write(i, 5, (tot_cur_period_hpp + tot_prev_period_hpp + tot_last_period_hpp) * -1, money2)

            i = i + 2
            sheet2.write(i, 0, "Cost of Production", format0)
            i = i + 1
            sheet2.write(i, 1, "Material Cost", format0)
            tot_cur_period_cost = 0
            tot_prev_period_cost = 0
            tot_last_period_cost = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Material Cost')])
            for obj in lines:
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Direct Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Direct Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Indirect Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Indirect Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Transportation", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Transportation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Energy Production", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Energy Production')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Maintenance", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Maintenance')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Other Overhead", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Overhead')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Cost of Production', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_cost * -1, money)
            sheet2.write(i, 3, tot_prev_period_cost * -1, money)
            sheet2.write(i, 4, tot_last_period_cost * -1, money)
            sheet2.write(i, 5, (tot_cur_period_cost+tot_prev_period_cost+tot_last_period_cost) * -1, money2)

            i = i + 2
            gross_cur = 0
            gross_prev = 0
            gross_last = 0
            sheet2.write(i, 0, 'Gross Margin', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_cost + tot_last_period_hpp) * -1, money)

            gross_cur = (tot_cur_period_cost + tot_cur_period_hpp) * -1
            gross_prev= (tot_prev_period_cost + tot_prev_period_hpp) * -1
            gross_last= (tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, gross_cur+gross_prev+gross_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Operating Expenses", format0)
            tot_cur_period_exp = 0
            tot_prev_period_exp = 0
            tot_last_period_exp = 0

            i = i + 1
            sheet2.write(i, 1, "Admin Personel Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Admin Personel Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Facility Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Facility Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Vehicle Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Vehicle Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "IT Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'IT Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "General Admin Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'General Admin Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Operating Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_exp, money)
            sheet2.write(i, 3, tot_prev_period_exp, money)
            sheet2.write(i, 4, tot_last_period_exp, money)
            sheet2.write(i, 5, tot_cur_period_exp+tot_prev_period_exp+tot_last_period_exp, money2)

            i = i + 2
            ebitda_cur=0
            ebitda_prev=0
            ebitda_last=0
            sheet2.write(i, 0, 'EBITDA', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)
            ebitda_cur = (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebitda_prev= (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebitda_last= (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, ebitda_cur+ebitda_prev+ebitda_last, money2)

            i = i + 2
            sheet2.write(i, 0, "Depreciation", format0)
            tot_cur_period_dep = 0
            tot_prev_period_dep = 0
            tot_last_period_dep = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Depreciation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, "Amortization", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Amortization')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Depreciation and Amort.', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_dep * -1, money)
            sheet2.write(i, 3, tot_prev_period_dep * -1, money)
            sheet2.write(i, 4, tot_last_period_dep * -1, money)
            sheet2.write(i, 5, (tot_cur_period_dep + tot_prev_period_dep + tot_last_period_dep) * -1, money2)

            i = i + 2
            ebit_cur = 0
            ebit_prev= 0
            ebit_last= 0
            sheet2.write(i, 0, 'EBIT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            ebit_cur = (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebit_prev= (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebit_last= (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, ebit_cur+ebit_prev+ebit_last, money2)


            i = i + 2
            sheet2.write(i, 0, "Other Income/ Expenses", format0)
            tot_cur_other_ie = 0
            tot_prev_other_ie = 0
            tot_last_other_ie = 0

            i = i + 1
            sheet2.write(i, 1, "Other Income", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Profits on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Other Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Loss on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)


            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Other Income/ Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_other_ie * -1, money)
            sheet2.write(i, 3, tot_prev_other_ie * -1, money)
            sheet2.write(i, 4, tot_last_other_ie * -1, money)
            sheet2.write(i, 5, (tot_cur_other_ie + tot_prev_other_ie + tot_last_other_ie) * -1, money2)

            i = i + 2
            net_cur=0
            net_prev=0
            net_last=0
            sheet2.write(i, 0, 'Net Income/(loss)', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            net_cur = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            net_prev= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            net_last= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, net_cur + net_prev + net_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Taxes", format0)
            tot_cur_tax = 0
            tot_prev_tax = 0
            tot_last_tax = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Taxes')])
            for obj in lines:
                i = i + 1
                tot_cur_tax = tot_cur_tax + (obj.cur_period)
                tot_prev_tax = tot_prev_tax + (obj.prev_period)
                tot_last_tax = tot_last_tax + (obj.last_period)

                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, tot_cur_tax , money)
                sheet2.write(i, 3, tot_prev_tax , money)
                sheet2.write(i, 4, tot_last_tax , money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

            i = i + 2
            tot_eat_cur=0
            tot_eat_prev=0
            tot_eat_last=0
            sheet2.write(i, 0, 'EAT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            tot_eat_cur= (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            tot_eat_prev=(tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            tot_eat_last=(tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp)* -1

            sheet2.write(i, 5, tot_eat_cur + tot_eat_prev + tot_eat_last, money2)

            e_a_t = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            e_a_t2= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            e_a_t3= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
        # i = i + 2


        ##########QUARTER 3

        if quarter == 'q3':
            sheet2.write(4, 0, ' ', format1)
            sheet2.write(4, 1, ' ', format1)
            sheet2.write(4, 2, 'Jul', format1)
            sheet2.write(4, 3, 'Aug', format1)
            sheet2.write(4, 4, 'Sep', format1)
            sheet2.write(4, 5, 'Q3', format1)

            i = 5

            i = i + 1
            sheet2.write(i, 0, "Revenue", format0)
            tot_cur_period_hpp = 0
            tot_prev_period_hpp = 0
            tot_last_period_hpp = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Revenue')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_hpp = tot_cur_period_hpp + (obj.cur_period)
                tot_prev_period_hpp = tot_prev_period_hpp + (obj.prev_period)
                tot_last_period_hpp = tot_last_period_hpp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, 'Total Revenue', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_hpp * -1 , money)
            sheet2.write(i, 3, tot_prev_period_hpp * -1, money)
            sheet2.write(i, 4, tot_last_period_hpp * -1, money)
            sheet2.write(i, 5, (tot_cur_period_hpp + tot_prev_period_hpp + tot_last_period_hpp) * -1, money2)

            i = i + 2
            sheet2.write(i, 0, "Cost of Production", format0)
            i = i + 1
            sheet2.write(i, 1, "Material Cost", format0)
            tot_cur_period_cost = 0
            tot_prev_period_cost = 0
            tot_last_period_cost = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Material Cost')])
            for obj in lines:
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Direct Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Direct Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Indirect Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Indirect Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Transportation", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Transportation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Energy Production", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Energy Production')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Maintenance", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Maintenance')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Other Overhead", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Overhead')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Cost of Production', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_cost * -1, money)
            sheet2.write(i, 3, tot_prev_period_cost * -1, money)
            sheet2.write(i, 4, tot_last_period_cost * -1, money)
            sheet2.write(i, 5, (tot_cur_period_cost+tot_prev_period_cost+tot_last_period_cost) * -1, money2)

            i = i + 2
            gross_cur = 0
            gross_prev = 0
            gross_last = 0
            sheet2.write(i, 0, 'Gross Margin', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_cost + tot_last_period_hpp) * -1, money)

            gross_cur = (tot_cur_period_cost + tot_cur_period_hpp) * -1
            gross_prev= (tot_prev_period_cost + tot_prev_period_hpp) * -1
            gross_last= (tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, gross_cur+gross_prev+gross_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Operating Expenses", format0)
            tot_cur_period_exp = 0
            tot_prev_period_exp = 0
            tot_last_period_exp = 0

            i = i + 1
            sheet2.write(i, 1, "Admin Personel Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Admin Personel Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Facility Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Facility Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Vehicle Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Vehicle Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "IT Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'IT Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "General Admin Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'General Admin Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Operating Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_exp, money)
            sheet2.write(i, 3, tot_prev_period_exp, money)
            sheet2.write(i, 4, tot_last_period_exp, money)
            sheet2.write(i, 5, tot_cur_period_exp+tot_prev_period_exp+tot_last_period_exp, money2)

            i = i + 2
            ebitda_cur=0
            ebitda_prev=0
            ebitda_last=0
            sheet2.write(i, 0, 'EBITDA', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)
            ebitda_cur = (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebitda_prev= (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebitda_last= (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, ebitda_cur+ebitda_prev+ebitda_last, money2)

            i = i + 2
            sheet2.write(i, 0, "Depreciation", format0)
            tot_cur_period_dep = 0
            tot_prev_period_dep = 0
            tot_last_period_dep = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Depreciation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, "Amortization", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Amortization')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Depreciation and Amort.', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_dep * -1, money)
            sheet2.write(i, 3, tot_prev_period_dep * -1, money)
            sheet2.write(i, 4, tot_last_period_dep * -1, money)
            sheet2.write(i, 5, (tot_cur_period_dep + tot_prev_period_dep + tot_last_period_dep) * -1, money2)

            i = i + 2
            ebit_cur = 0
            ebit_prev= 0
            ebit_last= 0
            sheet2.write(i, 0, 'EBIT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            ebit_cur = (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebit_prev= (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebit_last= (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, ebit_cur+ebit_prev+ebit_last, money2)


            i = i + 2
            sheet2.write(i, 0, "Other Income/ Expenses", format0)
            tot_cur_other_ie = 0
            tot_prev_other_ie = 0
            tot_last_other_ie = 0

            i = i + 1
            sheet2.write(i, 1, "Other Income", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Profits on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Other Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Loss on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)


            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Other Income/ Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_other_ie * -1, money)
            sheet2.write(i, 3, tot_prev_other_ie * -1, money)
            sheet2.write(i, 4, tot_last_other_ie * -1, money)
            sheet2.write(i, 5, (tot_cur_other_ie + tot_prev_other_ie + tot_last_other_ie) * -1, money2)

            i = i + 2
            net_cur=0
            net_prev=0
            net_last=0
            sheet2.write(i, 0, 'Net Income/(loss)', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            net_cur = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            net_prev= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            net_last= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, net_cur + net_prev + net_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Taxes", format0)
            tot_cur_tax = 0
            tot_prev_tax = 0
            tot_last_tax = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Taxes')])
            for obj in lines:
                i = i + 1
                tot_cur_tax = tot_cur_tax + (obj.cur_period)
                tot_prev_tax = tot_prev_tax + (obj.prev_period)
                tot_last_tax = tot_last_tax + (obj.last_period)

                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, tot_cur_tax , money)
                sheet2.write(i, 3, tot_prev_tax , money)
                sheet2.write(i, 4, tot_last_tax , money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

            i = i + 2
            tot_eat_cur=0
            tot_eat_prev=0
            tot_eat_last=0
            sheet2.write(i, 0, 'EAT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            tot_eat_cur= (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            tot_eat_prev=(tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            tot_eat_last=(tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp)* -1

            sheet2.write(i, 5, tot_eat_cur + tot_eat_prev + tot_eat_last, money2)

            e_a_t = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            e_a_t2= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            e_a_t3= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
        # i = i + 2



        ##########QUARTER 4

        if quarter == 'q4':
            sheet2.write(4, 0, ' ', format1)
            sheet2.write(4, 1, ' ', format1)
            sheet2.write(4, 2, 'Oct', format1)
            sheet2.write(4, 3, 'Nov', format1)
            sheet2.write(4, 4, 'Dec', format1)
            sheet2.write(4, 5, 'Q4', format1)

            i = 5

            i = i + 1
            sheet2.write(i, 0, "Revenue", format0)
            tot_cur_period_hpp = 0
            tot_prev_period_hpp = 0
            tot_last_period_hpp = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Revenue')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_hpp = tot_cur_period_hpp + (obj.cur_period)
                tot_prev_period_hpp = tot_prev_period_hpp + (obj.prev_period)
                tot_last_period_hpp = tot_last_period_hpp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, 'Total Revenue', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_hpp * -1 , money)
            sheet2.write(i, 3, tot_prev_period_hpp * -1, money)
            sheet2.write(i, 4, tot_last_period_hpp * -1, money)
            sheet2.write(i, 5, (tot_cur_period_hpp + tot_prev_period_hpp + tot_last_period_hpp) * -1, money2)

            i = i + 2
            sheet2.write(i, 0, "Cost of Production", format0)
            i = i + 1
            sheet2.write(i, 1, "Material Cost", format0)
            tot_cur_period_cost = 0
            tot_prev_period_cost = 0
            tot_last_period_cost = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Material Cost')])
            for obj in lines:
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Direct Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Direct Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Indirect Labor Cost", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Indirect Labor Cost')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Transportation", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Transportation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Energy Production", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Energy Production')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Maintenance", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Maintenance')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)


            i = i + 1
            sheet2.write(i, 1, "Other Overhead", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Overhead')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
                tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)
                tot_last_period_cost = tot_last_period_cost + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Cost of Production', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_cost * -1, money)
            sheet2.write(i, 3, tot_prev_period_cost * -1, money)
            sheet2.write(i, 4, tot_last_period_cost * -1, money)
            sheet2.write(i, 5, (tot_cur_period_cost+tot_prev_period_cost+tot_last_period_cost) * -1, money2)

            i = i + 2
            gross_cur = 0
            gross_prev = 0
            gross_last = 0
            sheet2.write(i, 0, 'Gross Margin', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_cost + tot_last_period_hpp) * -1, money)

            gross_cur = (tot_cur_period_cost + tot_cur_period_hpp) * -1
            gross_prev= (tot_prev_period_cost + tot_prev_period_hpp) * -1
            gross_last= (tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, gross_cur+gross_prev+gross_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Operating Expenses", format0)
            tot_cur_period_exp = 0
            tot_prev_period_exp = 0
            tot_last_period_exp = 0

            i = i + 1
            sheet2.write(i, 1, "Admin Personel Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Admin Personel Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Facility Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Facility Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Vehicle Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Vehicle Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "IT Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'IT Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "General Admin Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'General Admin Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
                tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
                tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)
                tot_last_period_exp = tot_last_period_exp + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Operating Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_exp, money)
            sheet2.write(i, 3, tot_prev_period_exp, money)
            sheet2.write(i, 4, tot_last_period_exp, money)
            sheet2.write(i, 5, tot_cur_period_exp+tot_prev_period_exp+tot_last_period_exp, money2)

            i = i + 2
            ebitda_cur=0
            ebitda_prev=0
            ebitda_last=0
            sheet2.write(i, 0, 'EBITDA', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)
            ebitda_cur = (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebitda_prev= (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebitda_last= (tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, ebitda_cur+ebitda_prev+ebitda_last, money2)

            i = i + 2
            sheet2.write(i, 0, "Depreciation", format0)
            tot_cur_period_dep = 0
            tot_prev_period_dep = 0
            tot_last_period_dep = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Depreciation')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 1
            sheet2.write(i, 0, "Amortization", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Amortization')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
                tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)
                tot_last_period_dep = tot_last_period_dep + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Depreciation and Amort.', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_period_dep * -1, money)
            sheet2.write(i, 3, tot_prev_period_dep * -1, money)
            sheet2.write(i, 4, tot_last_period_dep * -1, money)
            sheet2.write(i, 5, (tot_cur_period_dep + tot_prev_period_dep + tot_last_period_dep) * -1, money2)

            i = i + 2
            ebit_cur = 0
            ebit_prev= 0
            ebit_last= 0
            sheet2.write(i, 0, 'EBIT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            ebit_cur = (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            ebit_prev= (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            ebit_last= (tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1

            sheet2.write(i, 5, ebit_cur+ebit_prev+ebit_last, money2)


            i = i + 2
            sheet2.write(i, 0, "Other Income/ Expenses", format0)
            tot_cur_other_ie = 0
            tot_prev_other_ie = 0
            tot_last_other_ie = 0

            i = i + 1
            sheet2.write(i, 1, "Other Income", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Profits on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Income')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 1
            sheet2.write(i, 1, "Other Expenses", format0)
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Interest Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Loss on Currency Exchange')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non Operating Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)


            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Extraordinary Expenses')])
            for obj in lines:
                i = i + 1
                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, obj.cur_period * -1, money)
                sheet2.write(i, 3, obj.prev_period * -1, money)
                sheet2.write(i, 4, obj.last_period * -1, money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

                tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
                tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)
                tot_last_other_ie = tot_last_other_ie + (obj.last_period)

            i = i + 2
            sheet2.write(i, 0, 'Total Other Income/ Expenses', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, tot_cur_other_ie * -1, money)
            sheet2.write(i, 3, tot_prev_other_ie * -1, money)
            sheet2.write(i, 4, tot_last_other_ie * -1, money)
            sheet2.write(i, 5, (tot_cur_other_ie + tot_prev_other_ie + tot_last_other_ie) * -1, money2)

            i = i + 2
            net_cur=0
            net_prev=0
            net_last=0
            sheet2.write(i, 0, 'Net Income/(loss)', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            net_cur = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            net_prev= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            net_last= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
            sheet2.write(i, 5, net_cur + net_prev + net_last, money2)



            i = i + 2
            sheet2.write(i, 0, "Taxes", format0)
            tot_cur_tax = 0
            tot_prev_tax = 0
            tot_last_tax = 0
            lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Taxes')])
            for obj in lines:
                i = i + 1
                tot_cur_tax = tot_cur_tax + (obj.cur_period)
                tot_prev_tax = tot_prev_tax + (obj.prev_period)
                tot_last_tax = tot_last_tax + (obj.last_period)

                sheet2.write(i, 0, obj.code, formatcode)
                sheet2.write(i, 1, obj.name, format2)
                sheet2.write(i, 2, tot_cur_tax , money)
                sheet2.write(i, 3, tot_prev_tax , money)
                sheet2.write(i, 4, tot_last_tax , money)
                sheet2.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)

            i = i + 2
            tot_eat_cur=0
            tot_eat_prev=0
            tot_eat_last=0
            sheet2.write(i, 0, 'EAT', format0)
            # sheet.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
            sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)
            sheet2.write(i, 4, (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1, money)

            tot_eat_cur= (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            tot_eat_prev=(tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            tot_eat_last=(tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp)* -1

            sheet2.write(i, 5, tot_eat_cur + tot_eat_prev + tot_eat_last, money2)

            e_a_t = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
            e_a_t2= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
            e_a_t3= (tot_last_other_ie + tot_last_period_dep + tot_last_period_exp + tot_last_period_cost + tot_last_period_hpp) * -1
        # i = i + 2

        sheet = workbook.add_worksheet('Balance Sheet')
        sheet.set_column(0, 0, 10)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 15)


        sheet.write(0, 0, 'PT. PENYELESAIAN MASALAH PROPERTY', format1)
        sheet.write(1, 0, 'STATEMENT OF FINANCIAL POSITION', format1)
        sheet.write(2, 0, data['form']['tahun'], format0)

    
        ##########QUARTER 1

        if quarter == 'q1':
            sheet.write(4, 0, ' ', format1)
            sheet.write(4, 1, ' ', format1)
            sheet.write(4, 2, 'Jan', format1)
            sheet.write(4, 3, 'Feb', format1)
            sheet.write(4, 4, 'Mar', format1)
            sheet.write(4, 5, 'Q1', format3)


        if quarter == 'q2':
            sheet.write(4, 0, ' ', format1)
            sheet.write(4, 1, ' ', format1)
            sheet.write(4, 2, 'Apr', format1)
            sheet.write(4, 3, 'May', format1)
            sheet.write(4, 4, 'Jun', format1)
            sheet.write(4, 5, 'Q2', format3)

        if quarter == 'q3':
            sheet.write(4, 0, ' ', format1)
            sheet.write(4, 1, ' ', format1)
            sheet.write(4, 2, 'Jul', format1)
            sheet.write(4, 3, 'Aug', format1)
            sheet.write(4, 4, 'Sep', format1)
            sheet.write(4, 5, 'Q3', format3)

        if quarter == 'q4':
            sheet.write(4, 0, ' ', format1)
            sheet.write(4, 1, ' ', format1)
            sheet.write(4, 2, 'Okt', format1)
            sheet.write(4, 3, 'Nov', format1)
            sheet.write(4, 4, 'Dec', format1)
            sheet.write(4, 5, 'Q4', format3)


        i=5
        tot_cur_period = 0
        tot_prev_period= 0
        tot_last_period= 0

        sheet.write(i, 0, "Asset", format0)
        i = i + 1
        sheet.write(i, 0, "Current Assets", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Current Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Cash & Cash equivalents", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type','=','Cash & Cash equivalents')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Receivable", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('code', '>=', '112000'),('code', '<', '113000')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Other Receivable", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Receivable')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Prepayments", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Prepayments')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Prepaid Tax", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Prepaid Tax')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Inventory Stock Material", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Inventory Stock Material')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Inventory Semi Finished Goods", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Inventory Semi Finished Goods')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Inventory Sparepart", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Inventory Sparepart')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Other Current Assets", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Current Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_cur_period = tot_cur_period + (obj.cur_period)
            tot_prev_period = tot_prev_period + (obj.prev_period)
            tot_last_period = tot_last_period + (obj.last_period)

        i=i+2
        sheet.write(i, 0,'Total Current Assets', format0)
        sheet.write(i, 2, tot_cur_period, money)
        sheet.write(i, 3, tot_prev_period, money)
        sheet.write(i, 4, tot_last_period, money)
        sheet.write(i, 5, tot_cur_period + tot_prev_period + tot_last_period, money2)




        tot_non_cur_period = 0
        tot_non_prev_period= 0
        tot_non_last_period= 0

        i = i + 2
        sheet.write(i, 0, "Non-Current Assets", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non-Current Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)
            tot_non_last_period = tot_non_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Fixed Assets Acquisition", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Fixed Assets Acquisition')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)
            tot_non_last_period = tot_non_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Accumulation Depreciation", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Accumulation Depreciation')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)
            tot_non_last_period = tot_non_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Intangible Assets", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Intangible Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)
            tot_non_last_period = tot_non_last_period + (obj.last_period)

        
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Fixed Assets Land')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)
            tot_non_last_period = tot_non_last_period + (obj.last_period)

        lines = self.env['pr.balance_sheet_v3'].search([('code', '=', '124001')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)
            tot_non_last_period = tot_non_last_period + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Other Non Current Assets", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Non Current Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, money)
            sheet.write(i, 3, obj.prev_period, money)
            sheet.write(i, 4, obj.last_period, money)
            sheet.write(i, 5, obj.cur_period + obj.prev_period + obj.last_period, money2)
            tot_non_cur_period = tot_non_cur_period + (obj.cur_period)
            tot_non_prev_period = tot_non_prev_period + (obj.prev_period)
            tot_non_last_period = tot_non_last_period + (obj.last_period)

        i=i+2
        sheet.write(i, 0,'Total Non Current Assets', format0)
        sheet.write(i, 2, tot_non_cur_period, money)
        sheet.write(i, 3, tot_non_prev_period, money)
        sheet.write(i, 4, tot_non_last_period, money)
        sheet.write(i, 5, tot_non_cur_period+tot_non_prev_period+tot_non_last_period, money2)

        i=i+2
        asset_cur =0
        asset_prev=0
        asset_last=0
        sheet.write(i, 0,'Total Assets', format0)
        sheet.write(i, 2, (tot_cur_period+tot_non_cur_period), money)
        sheet.write(i, 3, (tot_prev_period+tot_non_prev_period), money)
        sheet.write(i, 4, (tot_last_period+tot_non_last_period), money)

        asset_cur = tot_cur_period+tot_non_cur_period
        asset_prev= tot_prev_period+tot_non_prev_period
        asset_last= tot_last_period+tot_non_last_period

        sheet.write(i, 5, asset_cur+asset_prev+asset_last, money2)



        i = i + 3
        sheet.write(i, 0, "Liabilities and Equity", format0)
        tot_cur_period_hutang = 0
        tot_prev_period_hutang = 0
        tot_last_period_hutang = 0

        tot_non_cur_period_hutang = 0
        tot_non_prev_period_hutang = 0
        tot_non_last_period_hutang = 0

        i = i + 1
        sheet.write(i, 0, "Current Liabilities", format1)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Current Liabilities')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)


        i = i + 1
        sheet.write(i, 1, "Payable", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Payable')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)


        i = i + 1
        sheet.write(i, 1, "Other Payable", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Payable')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Tax Payable", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Tax Payable')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Accruals And Deferred Income", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Accruals And Deferred Income')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "S/T Loans", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'S/T Loans')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "S/T Provision", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'S/T Provision')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 2
        sheet.write(i, 0, 'Total Current Liabilities', format0)
        # sheet.write(i, 1, obj.name, format2) 
        sheet.write(i, 2, tot_cur_period_hutang * -1, money)
        sheet.write(i, 3, tot_prev_period_hutang * -1, money)
        sheet.write(i, 4, tot_prev_period_hutang * -1, money)

        sheet.write(i, 5, tot_cur_period_hutang + tot_prev_period_hutang + tot_last_period_hutang * -1, money2)


        i = i + 2
        sheet.write(i, 0, "Non-Current Liabilities", format1)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Non-Current Liabilities')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "L/T Loans", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'L/T Loans')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "L/T Provision", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'L/T Provision')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Other Non Current Liabilities", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Non Current Liabilities')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_hutang = tot_cur_period_hutang + (obj.cur_period)
            tot_prev_period_hutang = tot_prev_period_hutang + (obj.prev_period)
            tot_last_period_hutang = tot_last_period_hutang + (obj.last_period)

        i = i + 2
        sheet.write(i, 0, 'Total Non-Current Liabilities', format0)
        sheet.write(i, 2, (tot_non_cur_period_hutang * -1), money)
        sheet.write(i, 3, (tot_non_prev_period_hutang * -1), money)
        sheet.write(i, 4, (tot_non_last_period_hutang * -1), money)

        sheet.write(i, 5, (tot_non_cur_period_hutang + tot_non_prev_period_hutang + tot_non_last_period_hutang) * -1, money2)


        i = i + 2
        sheet.write(i, 0, "Equity", format0)
        tot_cur_period_modal = 0
        tot_prev_period_modal = 0
        tot_last_period_modal = 0

        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Equity')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)
            tot_last_period_modal = tot_last_period_modal + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Share & Capital Reserves", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Share & Capital Reserve')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)
            tot_last_period_modal = tot_last_period_modal + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Dividend", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Dividend')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)
            tot_last_period_modal = tot_last_period_modal + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Profit/Loss Carried Forward", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Profit/Loss Carried Forward')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)
            tot_last_period_modal = tot_last_period_modal + (obj.last_period)


        i = i + 1
        sheet.write(i, 1, "Profit/Loss Of Period", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Profit/Loss Of Period')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)
            tot_last_period_modal = tot_last_period_modal + (obj.last_period)

        i = i + 1
        sheet.write(i, 1, "Other Equity Component", format0)
        lines = self.env['pr.balance_sheet_v3'].search([('account_type', '=', 'Other Equity Component')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, formatcode)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period * -1, money)
            sheet.write(i, 3, obj.prev_period * -1, money)
            sheet.write(i, 4, obj.last_period * -1, money)
            sheet.write(i, 5, (obj.cur_period + obj.prev_period + obj.last_period) * -1, money2)
            tot_cur_period_modal = tot_cur_period_modal + (obj.cur_period)
            tot_prev_period_modal = tot_prev_period_modal + (obj.prev_period)
            tot_last_period_modal = tot_last_period_modal + (obj.last_period)

        i = i + 2

        eq_cur = 0
        eq_prev= 0
        eq_last= 0
        sheet.write(i, 0, 'Total Equity', format0)
        sheet.write(i, 2, (tot_cur_period_modal + e_a_t) * -1, money)
        sheet.write(i, 3, (tot_prev_period_modal + e_a_t2)* -1, money)
        sheet.write(i, 4, (tot_last_period_modal + e_a_t3)* -1, money)
        eq_cur = (tot_cur_period_modal + e_a_t) * -1
        eq_prev= (tot_prev_period_modal + e_a_t2)* -1
        eq_last= (tot_last_period_modal + e_a_t3)* -1

        sheet.write(i, 5, (eq_cur + eq_prev + eq_last)* -1, money2)

        i = i + 2
        lae_cur = 0
        lae_prev= 0
        lae_last= 0
        sheet.write(i, 0, 'Total Liabilities and Equity', format0)
        sheet.write(i, 2, (tot_non_cur_period_hutang+tot_cur_period_hutang+tot_cur_period_modal-e_a_t) * -1, money)
        sheet.write(i, 3, (tot_non_prev_period_hutang+tot_prev_period_hutang+tot_prev_period_modal-e_a_t2) * -1, money)
        sheet.write(i, 4, (tot_non_prev_period_hutang+tot_prev_period_hutang+tot_prev_period_modal-e_a_t3) * -1, money)

        lae_cur = (tot_non_cur_period_hutang+tot_cur_period_hutang+tot_cur_period_modal-e_a_t) * -1
        lae_prev= (tot_non_prev_period_hutang+tot_prev_period_hutang+tot_prev_period_modal-e_a_t2) * -1
        lae_last= (tot_non_prev_period_hutang+tot_prev_period_hutang+tot_prev_period_modal-e_a_t3) * -1

        sheet.write(i, 5, (lae_cur + lae_prev + lae_last)* -1, money2)
