from odoo import models
from odoo.exceptions import UserError

class KitePWXlsx(models.AbstractModel):
    _name = 'report.ab_djbc_kite_xls.kite_pw_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('DJBC Laporan Penyelesaian Waste')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12, 'align':'right'})
        format4 = workbook.add_format({'font_size':12, 'align':'left'})
        sheet.merge_range('A1:N1', 'DJBC Laporan Penyelesaian Waste', format1)
        sheet.merge_range('A2:N2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format1)

        sheet.write(3,0,'No',format1)
        sheet.write(3,1,'No Pengeluaran',format1)
        sheet.write(3,2,'Tgl Pengeluaran',format1)
        sheet.write(3,3,'Kode Barang',format1)
        sheet.write(3,4,'Nama Barang',format1)
        sheet.write(3,5,'Satuan',format1)
        sheet.write(3,6,'Jumlah Disubkon',format1)
        sheet.write(3,7,'Penerima Subkon',format1)

        no = 1
        row = 4
        lines = self.env['djbc.kite_pw'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.nomor, format2)
            sheet.write(row, 2, obj.tanggal, format2)
            sheet.write(row, 3, obj.kode_barang, format4)
            sheet.write(row, 4, obj.nama_barang, format4)
            sheet.write(row, 5, obj.jumlah, format3)
            sheet.write(row, 6, obj.satuan, format2)
            sheet.write(row, 7, obj.gudang, format2)

            no = no+1
            row = row+1
