from odoo import models
from odoo.exceptions import UserError

class KitePengHPXlsx(models.AbstractModel):
    _name = 'report.ab_djbc_kite_xls.kite_penghp_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('DJBC Laporan Pengeluaran Hasil Produksi')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12, 'align':'right'})
        format4 = workbook.add_format({'font_size':12, 'align':'left'})
        sheet.merge_range('A1:N1', 'DJBC Laporan Pengeluaran Hasil Produksi', format1)
        sheet.merge_range('A2:N2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format1)

        sheet.write(3,0,'No',format1)
        sheet.write(3,1,'No Peb',format1)
        sheet.write(3,2,'Tgl Peb',format1)
        sheet.write(3,3,'Mata Uang',format1)
        sheet.write(3,4,'Negara Tujuan',format1)
        sheet.write(3,5,'No Pengeluaran',format1)
        sheet.write(3,6,'Tgl Pengeluaran',format1)
        sheet.write(3,7,'Kode Barang',format1)
        sheet.write(3,8,'Nama Barang',format1)
        sheet.write(3,9,'Jumlah',format1)
        sheet.write(3,10,'Satuan',format1)
        sheet.write(3,11,'Pembeli',format1)
        sheet.write(3,12,'Nilai',format1)
        sheet.write(3,13,'DJBC',format1)

        no = 1
        row = 4
        lines = self.env['djbc.kite_penghp'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.no_peb, format2)
            sheet.write(row, 2, obj.tgl_peb, format2)
            sheet.write(row, 3, obj.mata_uang, format3)
            sheet.write(row, 4, obj.negara_tujuan, format2)
            sheet.write(row, 5, obj.no_pengeluaran, format2)
            sheet.write(row, 6, obj.tgl_pengeluaran, format2)
            sheet.write(row, 7, obj.kode_barang, format4)
            sheet.write(row, 8, obj.nama_barang, format4)
            sheet.write(row, 9, obj.jumlah, format3)
            sheet.write(row, 10, obj.satuan, format2)
            sheet.write(row, 11, obj.pembeli, format2)
            sheet.write(row, 12, obj.nilai, format3)
            sheet.write(row, 13, obj.djbc, format2)

            no = no+1
            row = row+1

