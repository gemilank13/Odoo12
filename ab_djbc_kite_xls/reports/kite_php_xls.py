from odoo import models
from odoo.exceptions import UserError

class KitePHPXlsx(models.AbstractModel):
    _name = 'report.ab_djbc_kite_xls.kite_php_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('DJBC Laporan Pemasukan Hasil Produksi')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12, 'align':'right'})
        format4 = workbook.add_format({'font_size':12, 'align':'left'})
        sheet.merge_range('A1:N1', 'DJBC Laporan Pemasukan Hasil Produksi', format1)
        sheet.merge_range('A2:N2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format1)

        sheet.write(3,0,'No',format1)
        sheet.write(3,1,'No Penerimaan',format1)
        sheet.write(3,2,'Tgl Penerimaan',format1)
        sheet.write(3,3,'Kode Barang',format1)
        sheet.write(3,4,'Nama Barang',format1)
        sheet.write(3,5,'Jumlah',format1)
        sheet.write(3,6,'Satuan',format1)
        sheet.write(3,7,'Jumlah Disubkon',format1)

        no = 1
        row = 4
        lines = self.env['djbc.kite_php'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.no_penerimaan, format2)
            sheet.write(row, 2, obj.tgl_penerimaan, format2)
            sheet.write(row, 3, obj.kode_barang, format4)
            sheet.write(row, 4, obj.nama_barang, format4)
            sheet.write(row, 5, obj.jumlah, format3)
            sheet.write(row, 6, obj.satuan, format2)
            sheet.write(row, 7, obj.jumlah_disubkon, format3)

            no = no+1
            row = row+1
