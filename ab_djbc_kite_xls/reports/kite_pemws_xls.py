from odoo import models
from odoo.exceptions import UserError

class KitePemWSXlsx(models.AbstractModel):
    _name = 'report.ab_djbc_kite_xls.kite_pemws_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('DJBC Laporan Pemakaian WIP Subkontrak')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12, 'align':'right'})
        format4 = workbook.add_format({'font_size':12, 'align':'left'})
        sheet.merge_range('A1:N1', 'DJBC Laporan Pemakaian WIP Subkontrak', format1)
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
        lines = self.env['djbc.kite_pemws'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.nomor_pengeluaran, format2)
            sheet.write(row, 2, obj.tanggal_pengeluaran, format2)
            sheet.write(row, 3, obj.kode_barang, format4)
            sheet.write(row, 4, obj.nama_barang, format4)
            sheet.write(row, 5, obj.satuan, format2)
            sheet.write(row, 6, obj.jumlah_disubkon, format3)
            sheet.write(row, 7, obj.penerima_subkon, format2)

            no = no+1
            row = row+1