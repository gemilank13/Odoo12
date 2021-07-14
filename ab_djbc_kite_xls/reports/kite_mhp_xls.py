from odoo import models
from odoo.exceptions import UserError

class KiteMhpXlsx(models.AbstractModel):
    _name = 'report.ab_djbc_kite_xls.kite_mhp_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('DJBC Laporan Mutasi Hasil Produksi')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12, 'align':'right'})
        format4 = workbook.add_format({'font_size':12, 'align':'left'})
        sheet.merge_range('A1:N1', 'DJBC Laporan Mutasi Hasil Produksi', format1)
        sheet.merge_range('A2:N2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format1)

        sheet.write(3,0,'No',format1)
        sheet.write(3,1,'Kode Barang',format1)
        sheet.write(3,2,'Nama Barang',format1)
        # sheet.write(3,3,'Satuan',format1)
        sheet.write(3,3,'Saldo Awal',format1)
        sheet.write(3,4,'Pemasukan',format1)
        sheet.write(3,5,'Pengeluaran',format1)
        sheet.write(3,6,'Penyesuaian',format1)
        sheet.write(3,7,'Stock Opname',format1)
        sheet.write(3,8,'Saldo Akhir',format1)
        sheet.write(3,9,'Selisih',format1)
        sheet.write(3,10,'Keterangan',format1)
        sheet.write(3,11,'Warehouse',format1)

        no = 1
        row = 4
        lines = self.env['djbc.kite_mhp'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.kode_barang, format4)
            sheet.write(row, 2, obj.nama_barang, format2)
            # sheet.write(row, 3, obj.satuan, format2)
            sheet.write(row, 3, obj.saldo_awal, format3)
            sheet.write(row, 4, obj.pemasukan, format3)

            sheet.write(row, 5, obj.pengeluaran, format3)
            sheet.write(row, 6, obj.penyesuaian, format3)
            sheet.write(row, 7, obj.stock_opname, format3)
            sheet.write(row, 8, obj.saldo_akhir, format3)
            sheet.write(row, 9, obj.selisih, format3)
            sheet.write(row, 10, obj.keterangan, format2)
            sheet.write(row, 11, obj.warehouse, format2)

            no = no+1
            row = row+1
        