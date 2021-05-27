from odoo import models
from odoo.exceptions import UserError

class PemasukanXlsx(models.AbstractModel):
    _name = 'report.ab_laporan_posisi.posisi_wip_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('Laporan Posisi WIP')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        sheet.merge_range('A1:G1', 'Laporan Posisi WIP', format1)
        sheet.merge_range('A2:G2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format1)

        sheet.write(3,0,'No',format1)
        sheet.write(3,1,'Tgl Penerimaan',format1)
        sheet.write(3,2,'Kode Barang',format1)
        sheet.write(3,3,'Nama Barang',format1)
        sheet.write(3,4,'Jumlah',format1)
        sheet.write(3,5,'Satuan',format1)
        sheet.write(3,6,'Warehouse',format1)

        no = 1
        row = 4
        lines = self.env['djbc.posisi.wip'].search([])
        for obj in lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, str(obj.tgl_penerimaan), format2)
            sheet.write(row, 2, obj.kode_barang, format2)
            sheet.write(row, 3, obj.nama_barang, format2)
            sheet.write(row, 4, obj.jumlah, format2)
            sheet.write(row, 5, obj.satuan, format2)
            sheet.write(row, 6, obj.warehouse, format2)

            no = no+1
            row = row+1
