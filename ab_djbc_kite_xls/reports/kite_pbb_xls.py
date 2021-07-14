from odoo import models
from odoo.exceptions import UserError

class KitePbbXlsx(models.AbstractModel):
    _name = 'report.ab_djbc_kite_xls.kite_pbb_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('DJBC Laporan Pemasukan Bahan Baku')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12, 'align':'right'})
        format4 = workbook.add_format({'font_size':12, 'align':'left'})
        sheet.merge_range('A1:N1', 'DJBC Laporan Pemasukan Bahan Baku', format1)
        sheet.merge_range('A2:N2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format1)

        sheet.write(3,0,'No',format1)
        sheet.write(3,1,'Jenis Dok',format1)
        sheet.write(3,2,'No Penerimaan',format1)
        # sheet.write(3,3,'Satuan',format1)
        sheet.write(3,3,'Tgl Penerimaan',format1)
        sheet.write(3,4,'Kode Barang',format1)
        sheet.write(3,5,'Nama Barang',format1)
        sheet.write(3,6,'Jumlah',format1)
        sheet.write(3,7,'Satuan',format1)
        sheet.write(3,8,'Gudang',format1)
        sheet.write(3,9,'Nilai',format1)
        sheet.write(3,10,'Negara Asal',format1)
        sheet.write(3,11,'Penerima Subkon',format1)
        sheet.write(3,11,'DJBC',format1)

        no = 1
        row = 4
        lines = self.env['djbc.kite_pbb'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.jenis_dok, format2)
            sheet.write(row, 2, obj.no_penerimaan, format2)
            # sheet.write(row, 3, obj.satuan, format2)
            sheet.write(row, 3, str(obj.tgl_penerimaan), format2)
            sheet.write(row, 4, obj.kode_barang, format2)

            sheet.write(row, 5, obj.nama_barang, format4)
            sheet.write(row, 6, obj.jumlah, format3)
            sheet.write(row, 7, obj.satuan, format2)
            sheet.write(row, 8, obj.gudang, format2)
            sheet.write(row, 9, obj.nilai, format3)
            sheet.write(row, 10, obj.negara_asal, format2)
            sheet.write(row, 11, obj.penerima_subkon, format2)
            sheet.write(row, 11, obj.djbc, format4)

            no = no+1
            row = row+1
        