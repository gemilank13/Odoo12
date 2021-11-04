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
        sheet2.set_column(1,1,40)
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

        formatcode2 = workbook.add_format({
            'align':'right',
            'font_size': 10,
            'bold': True,
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
        type_laporan = data['form']['type_laporan']

        sheet2.write(0, 0, 'PT PENYELESAIAN MASALAH PROPERTY', format0)
        sheet2.write(1, 0, 'INCOME STATEMENT', format0)
        sheet2.write(2, 0, type_laporan, format0)
        sheet2.write(3, 0, 'Current Period : ' + d_start+'-'+m_start+'-'+y_start + ' s.d. ' + d_end+'-'+m_end+'-'+y_end, format0)
        sheet2.write(4, 0, 'Year to Date: ' + d_start2+'-'+m_start2+'-'+y_start2 + ' s.d. ' + d_end2+'-'+m_end2+'-'+y_end2, format0)

        sheet2.write(6, 0, ' ', format1)
        sheet2.write(6, 1, ' ', format1)
        sheet2.write(6, 2, 'Current Period', format1)
        sheet2.write(6, 3, 'Year to Date', format1)

        tot_cur_period_pendapatan = 0
        tot_prev_period_pendapatan = 0

        i = 7

        tot_cur_gs = 0
        tot_prev_gs = 0

        i = i + 2
        sheet2.write(i, 0, "810999", format0)
        sheet2.write(i, 1, "Gross sales domestic from goods and services", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','810999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)


        i = i + 1
        sheet2.write(i, 0, "820999", format0)
        sheet2.write(i, 1, "Gross sales export from goods and services", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','820999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "830999", format0)
        sheet2.write(i, 1, "Gross sales group from goods and services", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','830999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "840999", format0)
        sheet2.write(i, 1, "Gross sales related comp from goods and services", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','840999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_gs = tot_cur_gs + (obj2.cur_period)
                    tot_prev_gs = tot_prev_gs + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '849999', format0)
        sheet2.write(i, 1, 'Gross sales from goods and services', format0)
        sheet2.write(i, 2, tot_cur_gs * -1, money)
        sheet2.write(i, 3, tot_prev_gs * -1, money)


        tot_cur_tns = 0
        tot_prev_tns = 0

        i = i + 2
        sheet2.write(i, 0, "870999", format0)
        sheet2.write(i, 1, "Total revenue deductions from goods and services", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','870999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_tns = tot_cur_tns + (obj2.cur_period)
                    tot_prev_tns = tot_prev_tns + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_tns = tot_cur_tns + (obj2.cur_period)
                    tot_prev_tns = tot_prev_tns + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '879999', format0)
        sheet2.write(i, 1, 'Total net sales from goods and services', format0)
        sheet2.write(i, 2, tot_cur_tns * -1, money)
        sheet2.write(i, 3, tot_prev_tns * -1, money)


        tot_cur_or = 0
        tot_prev_or = 0

        i = i + 2
        sheet2.write(i, 0, "880999", format0)
        sheet2.write(i, 1, "Inventory change finished/semi-finished goods", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','880999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_or = tot_cur_or + (obj2.cur_period)
                    tot_prev_or = tot_prev_or + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_or = tot_cur_or + (obj2.cur_period)
                    tot_prev_or = tot_prev_or + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "881999", format0)
        sheet2.write(i, 1, "Other operating Income", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','881999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_or = tot_cur_or + (obj2.cur_period)
                    tot_prev_or = tot_prev_or + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_or = tot_cur_or + (obj2.cur_period)
                    tot_prev_or = tot_prev_or + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '889999', format0)
        sheet2.write(i, 1, 'Operating revenue', format0)
        sheet2.write(i, 2, tot_cur_or * -1, money)
        sheet2.write(i, 3, tot_prev_or * -1, money)


        tot_cur_gross = 0
        tot_prev_gross = 0

        i = i + 2
        sheet2.write(i, 0, "300999", format0)
        sheet2.write(i, 1, "Material third", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','300999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_gross = tot_cur_gross + (obj2.cur_period)
                    tot_prev_gross = tot_prev_gross + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_gross = tot_cur_gross + (obj2.cur_period)
                    tot_prev_gross = tot_prev_gross + (obj2.prev_period)


        i = i + 1
        sheet2.write(i, 0, "310999", format0)
        sheet2.write(i, 1, "Material group", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','310999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_gross = tot_cur_gross + (obj2.cur_period)
                    tot_prev_gross = tot_prev_gross + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_gross = tot_cur_gross + (obj2.cur_period)
                    tot_prev_gross = tot_prev_gross + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "320999", format0)
        sheet2.write(i, 1, "Total material costs & energy", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','320999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_gross = tot_cur_gross + (obj2.cur_period)
                    tot_prev_gross = tot_prev_gross + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_gross = tot_cur_gross + (obj2.cur_period)
                    tot_prev_gross = tot_prev_gross + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '329999', format0)
        sheet2.write(i, 1, 'Gross Margin', format0)
        sheet2.write(i, 2, tot_cur_gross * -1, money)
        sheet2.write(i, 3, tot_prev_gross * -1, money)


        tot_cur_ebitda = 0
        tot_prev_ebitda = 0

        jml_data = 0
        jml_data2 = 0

        i = i + 2
        sheet2.write(i, 0, "400999", format0)
        sheet2.write(i, 1, "Personnel expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','400999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)
                    

        i = i + 1
        sheet2.write(i, 0, "410999", format0)
        sheet2.write(i, 1, "Sales expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','410999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "420999", format0)
        sheet2.write(i, 1, "Transport & logistics", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','420999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "430999", format0)
        sheet2.write(i, 1, "Advertising expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','430999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)


        i = i + 1
        sheet2.write(i, 0, "440999", format0)
        sheet2.write(i, 1, "Facility expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','440999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)


        i = i + 1
        sheet2.write(i, 0, "450999", format0)
        sheet2.write(i, 1, "Maintenance/Repair (excl. facility and vehicles)", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','450999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)


        i = i + 1
        sheet2.write(i, 0, "451999", format0)
        sheet2.write(i, 1, "Vehicles", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','451999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "452999", format0)
        sheet2.write(i, 1, "IT-Expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','452999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "460999", format0)
        sheet2.write(i, 1, "Administration expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','460999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

        
        i = i + 1
        sheet2.write(i, 0, "470099", format0)
        sheet2.write(i, 1, "Licensing", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','470099')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "470999", format0)
        sheet2.write(i, 1, "Total operating expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','470999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebitda = tot_cur_ebitda + (obj2.cur_period)
                    tot_prev_ebitda = tot_prev_ebitda + (obj2.prev_period)



        i = i + 2
        sheet2.write(i, 0, '479999', format0)
        sheet2.write(i, 1, 'EBITDA', format0)
        sheet2.write(i, 2, tot_cur_ebitda * -1, money)
        sheet2.write(i, 3, tot_prev_ebitda * -1, money)

        tot_cur_ebit = 0
        tot_prev_ebit = 0

        i = i + 2
        sheet2.write(i, 0, "490999", format0)
        sheet2.write(i, 1, "Depreciation fixed assets", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','490999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebit = tot_cur_ebit + (obj2.cur_period)
                    tot_prev_ebit = tot_prev_ebit + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebit = tot_cur_ebit + (obj2.cur_period)
                    tot_prev_ebit = tot_prev_ebit + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "491099", format0)
        sheet2.write(i, 1, "Amortization on immat. assets", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','491099')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebit = tot_cur_ebit + (obj2.cur_period)
                    tot_prev_ebit = tot_prev_ebit + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebit = tot_cur_ebit + (obj2.cur_period)
                    tot_prev_ebit = tot_prev_ebit + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '491999', format0)
        sheet2.write(i, 1, 'EBIT', format0)
        sheet2.write(i, 2, tot_cur_ebit * -1, money)
        sheet2.write(i, 3, tot_prev_ebit * -1, money)



        tot_cur_finin = 0
        tot_prev_finin = 0

        i = i + 2
        sheet2.write(i, 0, "901999", format0)
        sheet2.write(i, 1, "Interest income", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','901999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "900999", format0)
        sheet2.write(i, 1, "Dividend income", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','900999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "902999", format0)
        sheet2.write(i, 1, "Profit From Participations", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','902999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "903999", format0)
        sheet2.write(i, 1, "Profit On Securities", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','903999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "904999", format0)
        sheet2.write(i, 1, "Profit On Currency Exchange", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','904999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finin = tot_cur_finin + (obj2.cur_period)
                    tot_prev_finin = tot_prev_finin + (obj2.prev_period)


        i = i + 2
        sheet2.write(i, 0, '909999', format0)
        sheet2.write(i, 1, 'Financial Income', format0)
        sheet2.write(i, 2, tot_cur_finin * -1, money)
        sheet2.write(i, 3, tot_prev_finin * -1, money)


        tot_cur_finex = 0
        tot_prev_finex = 0

        i = i + 2
        sheet2.write(i, 0, "910999", format0)
        sheet2.write(i, 1, "Interest Expenses", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','910999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "911999", format0)
        sheet2.write(i, 1, "Losses From Participations", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','911999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "912999", format0)
        sheet2.write(i, 1, "Losses On Securities", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','912999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "913999", format0)
        sheet2.write(i, 1, "Losses On Currency Exchange", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','913999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_finex = tot_cur_finex + (obj2.cur_period)
                    tot_prev_finex = tot_prev_finex + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '919999', format0)
        sheet2.write(i, 1, 'Financial Expenses', format0)
        sheet2.write(i, 2, tot_cur_finex * -1, money)
        sheet2.write(i, 3, tot_prev_finex * -1, money)



        tot_cur_ebt = 0
        tot_prev_ebt = 0

        i = i + 2
        sheet2.write(i, 0, "920999", format0)
        sheet2.write(i, 1, "Non-operating result", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','920999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebt = tot_cur_ebt + (obj2.cur_period)
                    tot_prev_ebt = tot_prev_ebt + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebt = tot_cur_ebt + (obj2.cur_period)
                    tot_prev_ebt = tot_prev_ebt + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "921099", format0)
        sheet2.write(i, 1, "Extraordinary result", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','921099')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebt = tot_cur_ebt + (obj2.cur_period)
                    tot_prev_ebt = tot_prev_ebt + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebt = tot_cur_ebt + (obj2.cur_period)
                    tot_prev_ebt = tot_prev_ebt + (obj2.prev_period)

        i = i + 1
        sheet2.write(i, 0, "939999", format0)
        sheet2.write(i, 1, "IC-postings Group", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','939999')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_ebt = tot_cur_ebt + (obj2.cur_period)
                    tot_prev_ebt = tot_prev_ebt + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_ebt = tot_cur_ebt + (obj2.cur_period)
                    tot_prev_ebt = tot_prev_ebt + (obj2.prev_period)



        i = i + 2
        sheet2.write(i, 0, '949999', format0)
        sheet2.write(i, 1, 'Profit before taxes (EBT)', format0)
        sheet2.write(i, 2, tot_cur_ebt * -1, money)
        sheet2.write(i, 3, tot_prev_ebt * -1, money)


        tot_cur_tax = 0
        tot_prev_tax = 0

        i = i + 2
        sheet2.write(i, 0, "950099", format0)
        sheet2.write(i, 1, "Taxes", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','950099')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_tax = tot_cur_tax + (obj2.cur_period)
                    tot_prev_tax = tot_prev_tax + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_tax = tot_cur_tax + (obj2.cur_period)
                    tot_prev_tax = tot_prev_tax + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '959999', format0)
        sheet2.write(i, 1, 'Net profit before minority interests', format0)
        sheet2.write(i, 2, tot_cur_tax * -1, money)
        sheet2.write(i, 3, tot_prev_tax * -1, money)


        tot_cur_netin = 0
        tot_prev_netin = 0

        i = i + 2
        sheet2.write(i, 0, "990001", format0)
        sheet2.write(i, 1, "Minority interests", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','990001')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code_prefix, formatcode2)
            sheet2.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                if type_laporan == 'PMP' :
                    i = i + 1
                    sheet2.write(i, 0, obj2.code, formatcode)
                    sheet2.write(i, 1, obj2.name, format2)
                    sheet2.write(i, 2, obj2.cur_period, money)
                    sheet2.write(i, 3, obj2.prev_period, money)
                    tot_cur_netin = tot_cur_netin + (obj2.cur_period)
                    tot_prev_netin = tot_prev_netin + (obj2.prev_period)

                if type_laporan == 'COGNOS' :

                    sheet2.write(i, 2, (obj2.cur_period), money)
                    sheet2.write(i, 3, (obj2.prev_period), money)
                    tot_cur_netin = tot_cur_netin + (obj2.cur_period)
                    tot_prev_netin = tot_prev_netin + (obj2.prev_period)

        i = i + 2
        sheet2.write(i, 0, '999999', format0)
        sheet2.write(i, 1, 'Net Income', format0)
        sheet2.write(i, 2, tot_cur_netin * -1, money)
        sheet2.write(i, 3, tot_prev_netin * -1, money)

                
        # i = i + 2
        # sheet2.write(i, 0, "Cost of Production", format0)

        # i = i + 1
        # sheet2.write(i, 1, "Material Cost", format0)
        # tot_cur_period_cost = 0
        # tot_prev_period_cost = 0
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Material Cost')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
        #     tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        # i = i + 1
        # sheet2.write(i, 1, "Direct Labor Cost", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Direct Labor Cost')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
        #     tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        # i = i + 1
        # sheet2.write(i, 1, "Indirect Labor Cost", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Indirect Labor Cost')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
        #     tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)

        # i = i + 1
        # sheet2.write(i, 1, "Transportation", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Transportation')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
        #     tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        # i = i + 1
        # sheet2.write(i, 1, "Energy Production", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Energy Production')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
        #     tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        # i = i + 1
        # sheet2.write(i, 1, "Maintenance", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Maintenance')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
        #     tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        # i = i + 1
        # sheet2.write(i, 1, "Other Overhead", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Overhead')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_cost = tot_cur_period_cost + (obj.cur_period)
        #     tot_prev_period_cost = tot_prev_period_cost + (obj.prev_period)


        # i = i + 2
        # sheet2.write(i, 0, 'Total Cost of Production', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, tot_cur_period_cost * -1, money)
        # sheet2.write(i, 3, tot_prev_period_cost * -1, money)

        # i = i + 2
        # sheet2.write(i, 0, 'Gross Margin', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, (tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        # sheet2.write(i, 3, (tot_prev_period_cost + tot_prev_period_hpp) * -1, money)


        # i = i + 2
        # sheet2.write(i, 0, "Operating Expenses", format0)
        # tot_cur_period_exp = 0
        # tot_prev_period_exp = 0

        # i = i + 1
        # sheet2.write(i, 1, "Admin Personel Expenses", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Admin Personel Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period , money)
        #     sheet2.write(i, 3, obj.prev_period, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
        #     tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        # i = i + 1
        # sheet2.write(i, 1, "Facility Expenses", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Facility Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period , money)
        #     sheet2.write(i, 3, obj.prev_period, money)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
        #     tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        # i = i + 1
        # sheet2.write(i, 1, "Vehicle Expenses", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Vehicle Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period , money)
        #     sheet2.write(i, 3, obj.prev_period, money)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
        #     tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        # i = i + 1
        # sheet2.write(i, 1, "IT Expenses", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'IT Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period , money)
        #     sheet2.write(i, 3, obj.prev_period, money)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
        #     tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        # i = i + 1
        # sheet2.write(i, 1, "General Admin Expenses", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'General Admin Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period , money)
        #     sheet2.write(i, 3, obj.prev_period, money)
        #     tot_cur_period_exp = tot_cur_period_exp + (obj.cur_period)
        #     tot_prev_period_exp = tot_prev_period_exp + (obj.prev_period)

        # i = i + 2
        # sheet2.write(i, 0, 'Total Operating Expenses', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, tot_cur_period_exp, money)
        # sheet2.write(i, 3, tot_prev_period_exp, money)

        # i = i + 2
        # sheet2.write(i, 0, 'EBITDA', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, (tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        # sheet2.write(i, 3, (tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)


        # i = i + 2
        # sheet2.write(i, 0, "Depreciation", format0)
        # tot_cur_period_dep = 0
        # tot_prev_period_dep = 0
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Depreciation')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
        #     tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)

        # i = i + 1
        # sheet2.write(i, 0, "Amortization", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Amortization')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_period_dep = tot_cur_period_dep + (obj.cur_period)
        #     tot_prev_period_dep = tot_prev_period_dep + (obj.prev_period)

        # i = i + 2
        # sheet2.write(i, 0, 'Total Depreciation and Amort.', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, tot_cur_period_dep * -1, money)
        # sheet2.write(i, 3, tot_prev_period_dep * -1, money)

        # i = i + 2
        # sheet2.write(i, 0, 'EBIT', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, (tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        # sheet2.write(i, 3, (tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)

        # i = i + 2
        # sheet2.write(i, 0, "Other Income/ Expenses", format0)
        # tot_cur_other_ie = 0
        # tot_prev_other_ie = 0

        # i = i + 1
        # sheet2.write(i, 1, "Other Income", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Interest Income')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Profits on Currency Exchange')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non Operating Income')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Extraordinary Income')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)


        # i = i + 1
        # sheet2.write(i, 1, "Other Expenses", format0)
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Interest Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Loss on Currency Exchange')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)

        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non Operating Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)


        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Extraordinary Expenses')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, obj.cur_period * -1, money)
        #     sheet2.write(i, 3, obj.prev_period * -1, money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
        #     tot_cur_other_ie = tot_cur_other_ie + (obj.cur_period)
        #     tot_prev_other_ie = tot_prev_other_ie + (obj.prev_period)


        # i = i + 2
        # sheet2.write(i, 0, 'Total Other Income/ Expenses', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, tot_cur_other_ie * -1, money)
        # sheet2.write(i, 3, tot_prev_other_ie * -1, money)

        # i = i + 2
        # sheet2.write(i, 0, 'Net Income/(loss)', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        # sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)


        # i = i + 2
        # sheet2.write(i, 0, "Taxes", format0)
        # tot_cur_tax = 0
        # tot_prev_tax = 0
        # lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Taxes')])
        # for obj in lines:
        #     # if obj.cur_period==0 and obj.prev_period==0:
        #     #     continue
        #     i = i + 1
        #     tot_cur_tax = tot_cur_tax + (obj.cur_period)
        #     tot_prev_tax = tot_prev_tax + (obj.prev_period)

        #     sheet2.write(i, 0, obj.code, formatcode)
        #     sheet2.write(i, 1, obj.name, format2)
        #     sheet2.write(i, 2, tot_cur_tax , money)
        #     sheet2.write(i, 3, tot_prev_tax , money)
        #     # sheet2.write(i, 4, obj.currency, format2)
        #     # sheet2.write(i, 5, obj.ori_cur_period, money)
        #     # sheet2.write(i, 6, obj.ori_prev_period, money)
            

        # i = i + 2
        # sheet2.write(i, 0, 'EAT', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet2.write(i, 2, (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1, money)
        # sheet2.write(i, 3, (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1, money)

        # e_a_t = (tot_cur_other_ie + tot_cur_period_dep + tot_cur_period_exp + tot_cur_period_cost + tot_cur_period_hpp) * -1
        # e_a_t2= (tot_prev_other_ie + tot_prev_period_dep + tot_prev_period_exp + tot_prev_period_cost + tot_prev_period_hpp) * -1
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
        sheet.set_column(1, 1, 40)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        # sheet.set_column(4, 4, 15)
        # sheet.set_column(5, 5, 15)

        

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
        tot_cur_inv = 0
        tot_prev_inv = 0
        tot_cur_fin = 0
        tot_prev_fin = 0


        i=6
        sheet.write(i, 0, "Asset", format0)
        i = i + 1
        sheet.write(i, 0, "Current Assets", format0)

        i = i + 1
        sheet.write(i, 0, "111099", format0)
        sheet.write(i, 1, "Cash & cash equivalents", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Cash & cash equivalents')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_period = tot_cur_period + (obj2.cur_period)
                tot_prev_period = tot_prev_period + (obj2.prev_period)



        i = i + 1
        sheet.write(i, 0, "112099", format0)
        sheet.write(i, 1, "Accounts receivables", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Accounts receivables')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_period = tot_cur_period + (obj2.cur_period)
                tot_prev_period = tot_prev_period + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "113099", format0)
        sheet.write(i, 1, "Other receivables", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Other receivables')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_period = tot_cur_period + (obj2.cur_period)
                tot_prev_period = tot_prev_period + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "114099", format0)
        sheet.write(i, 1, "S/T Loans", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','S/T Loans')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_period = tot_cur_period + (obj2.cur_period)
                tot_prev_period = tot_prev_period + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "120099", format0)
        sheet.write(i, 1, "Tobacco and raw material", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Tobacco and raw material')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_inv = tot_cur_inv + (obj2.cur_period)
                tot_prev_inv = tot_prev_inv + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "121099", format0)
        sheet.write(i, 1, "Semi finished goods", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Semi finished goods')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_inv = tot_cur_inv + (obj2.cur_period)
                tot_prev_inv = tot_prev_inv + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "122099", format0)
        sheet.write(i, 1, "Finished and trading goods", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Finished and trading goods')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_inv = tot_cur_inv + (obj2.cur_period)
                tot_prev_inv = tot_prev_inv + (obj2.prev_period)

        i=i+2
        sheet.write(i, 0,'120999', format0)
        sheet.write(i, 1,'Inventory', format0)
        sheet.write(i, 2, tot_cur_inv, money)
        sheet.write(i, 3, tot_prev_inv, money)

        i = i + 2
        sheet.write(i, 0, "130099", format0)
        sheet.write(i, 1, "Prepaid expenses and accrued income", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Prepaid expenses and accrued income')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_period = tot_cur_period + (obj2.cur_period)
                tot_prev_period = tot_prev_period + (obj2.prev_period)

        i=i+2
        sheet.write(i, 0,'130999', format0)
        sheet.write(i, 1,'Total Current Assets', format0)
        sheet.write(i, 2, (tot_cur_period + tot_cur_inv), money)
        sheet.write(i, 3, (tot_prev_period + tot_prev_inv), money)


        # i = i + 2
        # sheet.write(i, 0, "Non-Current Assets", format0)

        i = i + 2
        sheet.write(i, 0, "161099", format0)
        sheet.write(i, 1, "Participations", format0)
        lines = self.env['account.group'].search([('parent_id.name','=','Participations')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_fin = tot_cur_fin + (obj2.cur_period)
                tot_prev_fin = tot_prev_fin + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "162099", format0)
        sheet.write(i, 1, "Deferred taxes", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','162099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_fin = tot_cur_fin + (obj2.cur_period)
                tot_prev_fin = tot_prev_fin + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "163099", format0)
        sheet.write(i, 1, "L/T loans", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','163099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_fin = tot_cur_fin + (obj2.cur_period)
                tot_prev_fin = tot_prev_fin + (obj2.prev_period)

        i=i+2
        sheet.write(i, 0,'163999', format0)
        sheet.write(i, 1,'Financial Assets', format0)
        sheet.write(i, 2, tot_cur_fin, money)
        sheet.write(i, 3, tot_prev_fin, money)



        tot_cur_ppq = 0
        tot_prev_ppq = 0

        i = i + 2
        sheet.write(i, 0, "170009", format0)
        sheet.write(i, 1, "Machinery & production equipment", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','170009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)


        i = i + 1
        sheet.write(i, 0, "171009", format0)
        sheet.write(i, 1, "Cars & vehicles", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','171009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "172009", format0)
        sheet.write(i, 1, "IT & telecom equipment", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','172009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)


        i = i + 1
        sheet.write(i, 0, "174009", format0)
        sheet.write(i, 1, "Office equipment (incl. shop)", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','174009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)


        i = i + 1
        sheet.write(i, 0, "176009", format0)
        sheet.write(i, 1, "Operational buildings (incl. land)", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','176009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)


        i = i + 1
        sheet.write(i, 0, "177009", format0)
        sheet.write(i, 1, "Farm", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','177009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)


        i = i + 1
        sheet.write(i, 0, "178009", format0)
        sheet.write(i, 1, "Greenhouse", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','178009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "179009", format0)
        sheet.write(i, 1, "Non operational buildings", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','179009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)


        i = i + 1
        sheet.write(i, 0, "179009", format0)
        sheet.write(i, 1, "Non operational buildings", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','179009')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_cur_ppq = tot_cur_ppq + (obj2.cur_period)
                tot_prev_ppq = tot_cur_ppq + (obj2.prev_period)


        i=i+2
        sheet.write(i, 0,'170099', format0)
        sheet.write(i, 1,'Property, plant and equipment', format0)
        sheet.write(i, 2, tot_cur_ppq, money)
        sheet.write(i, 3, tot_prev_ppq, money)


        i = i + 2
        sheet.write(i, 0, "180099", format0)
        sheet.write(i, 1, "Intangible assets", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','180099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period, money)
                sheet.write(i, 3, obj2.prev_period, money)
                tot_non_cur_period = tot_non_cur_period + (obj2.cur_period)
                tot_non_prev_period = tot_non_prev_period + (obj2.prev_period)


        i=i+2
        sheet.write(i, 0,'190099', format0)
        sheet.write(i, 1,'Total non-current assets', format0)
        sheet.write(i, 2, (tot_non_cur_period + tot_cur_ppq + tot_cur_fin), money)
        sheet.write(i, 3, (tot_non_prev_period + tot_prev_ppq + tot_prev_fin), money)

        i=i+2
        sheet.write(i, 0,'199999', format0)
        sheet.write(i, 1,'Total assets', format0)
        sheet.write(i, 2, (tot_cur_period + tot_non_cur_period + tot_cur_ppq + tot_cur_fin), money)
        sheet.write(i, 3, (tot_prev_period + tot_non_prev_period + tot_prev_ppq + tot_prev_fin), money)


       


        i = i + 3
        sheet.write(i, 0, "Liabilities and Equity", format0)
        tot_cur_period_hutang = 0
        tot_prev_period_hutang = 0
        tot_non_cur_period_hutang = 0
        tot_non_prev_period_hutang = 0

        i = i + 1
        sheet.write(i, 0, "211099", format0)
        sheet.write(i, 1, "Accounts payable", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','211099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "221099", format0)
        sheet.write(i, 1, "Other payables (non-interest bearing)", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','221099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "222099", format0)
        sheet.write(i, 1, "S/T loans interest bearing", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','222099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "223099", format0)
        sheet.write(i, 1, "Other liabilities interest bearing", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','223099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "223099", format0)
        sheet.write(i, 1, "Other liabilities interest bearing", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','223099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "230099", format0)
        sheet.write(i, 1, "S/T provisions", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','230099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "231099", format0)
        sheet.write(i, 1, "Accruals and deferred income", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','231099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "250099", format0)
        sheet.write(i, 1, "L/T loans & liabilities interest bearing", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','250099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "251099", format0)
        sheet.write(i, 1, "L/T loans & liabilities non-interest bearing", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','251099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "260099", format0)
        sheet.write(i, 1, "L/T provisions", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','260099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "261099", format0)
        sheet.write(i, 1, "Deferred tax liabilities", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','261099')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_period_hutang = tot_cur_period_hutang + (obj2.cur_period)
                tot_prev_period_hutang = tot_prev_period_hutang + (obj2.prev_period)


        i = i + 2
        sheet.write(i, 0, '261999', format0)
        sheet.write(i, 1, 'Total non-current liabilities', format0)
        sheet.write(i, 2, tot_cur_period_hutang * -1, money)
        sheet.write(i, 3, tot_prev_period_hutang * -1, money)

        i = i + 2
        sheet.write(i, 0, '279999', format0)
        sheet.write(i, 1, 'Total liabilities', format0)
        sheet.write(i, 2, tot_cur_period_hutang * -1, money)
        sheet.write(i, 3, tot_prev_period_hutang * -1, money)


        tot_cur_eq = 0
        tot_prev_eq= 0

        i = i + 2
        sheet.write(i, 0, "290999", format0)
        sheet.write(i, 1, "Total equity excl. minority", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','290999')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_eq = tot_cur_eq + (obj2.cur_period)
                tot_prev_eq = tot_prev_eq + (obj2.prev_period)

        i = i + 1
        sheet.write(i, 0, "280999", format0)
        sheet.write(i, 1, "Total equity incl. minority interests", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','280999')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_eq = tot_cur_eq + (obj2.cur_period)
                tot_prev_eq = tot_prev_eq + (obj2.prev_period)

        i = i + 2
        sheet.write(i, 0, '299999', format0)
        sheet.write(i, 1, 'Total liabilities and equity', format0)
        sheet.write(i, 2, (tot_cur_eq + tot_cur_period_hutang) * -1, money)
        sheet.write(i, 3, (tot_prev_eq + tot_prev_period_hutang) * -1, money)

        i = i + 1
        sheet.write(i, 0, "29999C", format0)
        sheet.write(i, 1, "BS-Difference", format0)
        lines = self.env['account.group'].search([('parent_id.code_prefix','=','29999C')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code_prefix, formatcode2)
            sheet.write(i, 1, obj.name, format0)
            lines2 = self.env['pr.balance_sheet'].search([('group_id','=',obj.name)])
            for obj2 in lines2:
                i = i + 1
                sheet.write(i, 0, obj2.code, formatcode)
                sheet.write(i, 1, obj2.name, format2)
                sheet.write(i, 2, obj2.cur_period * -1, money)
                sheet.write(i, 3, obj2.prev_period * -1, money)
                tot_cur_eq = tot_cur_eq + (obj2.cur_period)
                tot_prev_eq = tot_prev_eq + (obj2.prev_period)
        
        
        # i = i + 2
        # sheet.write(i, 0, 'Total Current Liabilities', format0)
        # # sheet.write(i, 1, obj.name, format2) 
        # sheet.write(i, 2, tot_cur_period_hutang * -1, money)
        # sheet.write(i, 3, tot_prev_period_hutang * -1, money)

        # i = i + 2
        # sheet.write(i, 0, 'Total Non-Current Liabilities', format0)
        # # sheet.write(i, 1, obj.name, format2) 
        # sheet.write(i, 2, (tot_non_cur_period_hutang * -1), money)
        # sheet.write(i, 3, (tot_non_prev_period_hutang * -1), money)
        
        # i = i + 2
        # sheet.write(i, 0, 'Total Equity', format0)
        # # sheet.write(i, 1, obj.name, format2)
        # sheet.write(i, 2, (tot_cur_period_modal + e_a_t) * -1, money)
        # sheet.write(i, 3, (tot_prev_period_modal + e_a_t2)* -1, money)

        # i = i + 2
        # sheet.write(i, 0, 'Total Liabilities and Equity', format0)
        # # # sheet.write(i, 1, obj.name, format2)
        # # sheet.write(i, 1, (tot_cur_period_modal+tot_cur_period_hutang-tot_non_cur_period_hutang) * -1, money)
        # # sheet.write(i, 2, (tot_prev_period_modal+tot_prev_period_hutang-tot_non_prev_period_hutang) * -1, money)

        # sheet.write(i, 2, (tot_non_cur_period_hutang+tot_cur_period_hutang+tot_cur_period_modal-e_a_t) * -1, money)
        # sheet.write(i, 3, (tot_non_prev_period_hutang+tot_prev_period_hutang+tot_prev_period_modal-e_a_t2) * -1, money)


 