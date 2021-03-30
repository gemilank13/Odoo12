from odoo import models
# from odoo.exceptions import UserError

class ReceivementXlsx(models.AbstractModel):
    _name = 'report.ab_receiving_report2.receivement_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        sheet = workbook.add_worksheet('Receivement Item')
        format1 = workbook.add_format({'font_size':12, 'align':'center', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'center'})
        format3 = workbook.add_format({'font_size':12})
        sheet.merge_range('A1:H1','Receivement Item History',format1)
        # sheet.write(1,0, 'Periode: ' + str(data['form']['date_done']) + ' s.d. ' + str(data['form']['date_done']), format1)
        sheet.merge_range('A2:H2', 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_end']), format1)
        
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 15)

        sheet.write(3,0,'Tanggal Penerimaan',format2)
        sheet.write(3,1,'Nomor',format2)
        sheet.write(3,2,'Vendor/Supplier',format2)
        sheet.write(3,3,'Kode Barang',format2)
        sheet.write(3,4,'Deskripsi Barang',format2)
        sheet.write(3,5,'Quantitiy',format2)
        sheet.write(3,6,'Harga',format2)
        sheet.write(3,7,'UOM',format2)


        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        row = 4
        lines = self.env['stock.move'].search([('picking_type_id','=','Receipts'),('date','>=',date_start),('date','<=',date_end)])
        for obj in lines:
        	sheet.write(row, 0, str(obj.date), format3)
        	sheet.write(row, 1, obj.reference, format3)
        	sheet.write(row, 2, obj.picking_id.partner_id.name, format3)
        	sheet.write(row, 3, obj.product_id.default_code, format2)
        	sheet.write(row, 4, obj.product_id.name, format3)
        	sheet.write(row, 5, obj.product_uom_qty, format2)
        	sheet.write(row, 6, obj.price_unit, format2)
        	sheet.write(row, 7, obj.product_uom.name, format3)
        	row += 1