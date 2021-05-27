from odoo import models
from odoo.exceptions import UserError

class PemasukanXlsx(models.AbstractModel):
    _name = 'report.ab_laporan_posisi.posisi_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('Laporan Posisi Barang')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12, 'align':'left', 'bold':True})
        sheet.merge_range('A1:E1', 'Laporan Posisi Barang', format3)
        sheet.merge_range('A2:E2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format3)

        sheet.write(3,0,'No',format1)
        sheet.write(3,1,'Jenis Dok Masuk',format1)
        sheet.write(3,2,'No Dok Masuk',format1)
        sheet.write(3,3,'Tgl Dok Masuk',format1)
        sheet.write(3,4,'No Penerimaan',format1)
        sheet.write(3,5,'Tgl Penerimaan',format1)
        sheet.write(3,6,'Pengirim Barang',format1)
        sheet.write(3,7,'Pemilik Barang',format1)
        sheet.write(3,8,'Kode Barang',format1)
        sheet.write(3,9,'Nama Barang',format1)
        sheet.write(3,10,'Jumlah Pemasukan',format1)
        sheet.write(3,11,'Satuan Pemasukan',format1)
        sheet.write(3,12,'Nilai Masuk',format1)
        sheet.write(3,13,'Currency Masuk',format1)
        # sheet.write(3,5,'Jumlah',format1)
        # sheet.write(3,6,'Satuan',format1)
        # sheet.write(3,7,'Warehouse',format1)

        no = 1
        row = 4
        lines = self.env['djbc.nofas_posisi'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.jenis_dok_masuk, format2)
            sheet.write(row, 2, obj.no_dok_masuk, format2)
            sheet.write(row, 3, str(obj.tgl_dok_masuk), format2)
            sheet.write(row, 4, obj.no_penerimaan, format2)
            sheet.write(row, 5, str(obj.tgl_penerimaan), format2)
            sheet.write(row, 6, obj.pengirim, format2)
            sheet.write(row, 7, obj.pemilik, format2)
            sheet.write(row, 8, obj.kode_barang, format2)
            sheet.write(row, 9, obj.nama_barang, format2)
            sheet.write(row, 10, obj.jumlah_pemasukan, format2)
            sheet.write(row, 11, obj.satuan_pemasukan, format2)
            sheet.write(row, 12, obj.nilai_masuk, format2)
            sheet.write(row, 13, obj.currency_masuk, format2)
            # sheet.write(row, 4, obj.jumlah, format2)
            # sheet.write(row, 5, obj.satuan, format2)
            # sheet.write(row, 6, obj.warehouse, format2)

            no = no+1
            row = row+1
