from odoo import models
from odoo.exceptions import UserError
import xlsxwriter



class InvoiceXlsx(models.AbstractModel):
    _name = 'report.invoice_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

      #buka sheet
      sheet = workbook.add_worksheet('INVOICE OUT')

      #mengatur kolom
      sheet.set_column(0,0,15)
      sheet.set_column(1,1,15)
      sheet.set_column(2,2,25)
      sheet.set_column(3,3,15)
      sheet.set_column(4,4,10)
      sheet.set_column(5,5,10)
      sheet.set_column(6,6,15)

      #mengatur format text
      format1 = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Times',
      })

      format2 = workbook.add_format({
        'font_name': 'Times',
      })

      format3 = workbook.add_format({
        'font_name': 'Times',
        'align':'center',
        'valign':'vcenter'
      })
      format4 = workbook.add_format({
        'font_name': 'Times',
        'align':'right',
        'valign':'vcenter'
      })
      format0 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': True,
      })

      format5 = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'font_name': 'Times',
      })

      format6 = workbook.add_format({
        'bold': True,
        'align': ':left',
        'valign': 'vcenter',
        'font_name': 'Times',
      })


      head1 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': True,
        'border':1,
      })
      head2 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 16, 
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
      })

      head3 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': False,
        'align': 'center',
        'valign': 'vcenter',
      })


      head4 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': True,
      })


      text1 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': True,
        'border':1,
        'valign':'vcenter',
      })
      text2 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': False,
        'border':1,
        'align':'right',
      })

      text3 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': False,
        'border':1,
        'align':'left',
      })


      sheet.merge_range('A1:B1', 'MANUCTURER/SHIPPER', head1)
      sheet.merge_range('D1:G2', 'INVOICE', head2)
      # sheet.insert_image('A2', '/ab_invoice_sg/reports/smart_glove.PNG')
      # worksheet.insert_image('B2', 'python.png')

      sheet.merge_range('D3:E3', 'INVOICE NO.' , text1)
      sheet.merge_range('F3:G3', 'DATE.' , text1)
      sheet.merge_range('D4:E4', lines.number, text2)
      sheet.merge_range('F4:G4', str(lines.date_invoice) , text2)

      sheet.merge_range('D5:E5', 'PURCHASE ORDER NO.' , text1)
      sheet.merge_range('F5:G5', 'DATE.' , text1)
      sheet.merge_range('D6:E6', '', text2)
      sheet.merge_range('F6:G6', '' , text2)
      sheet.merge_range('D7:E7', '', text2)
      sheet.merge_range('F7:G7', '' , text2)
      sheet.merge_range('D8:E8', '', text2)
      sheet.merge_range('F8:G8', '' , text2)

      sheet.merge_range('D9:E9', 'SALES CTR NO.' , text1)
      sheet.merge_range('F9:G9', 'DATE.' , text1)
      sheet.merge_range('D10:E10', '', text2)
      sheet.merge_range('F10:G10', '' , text2)
      sheet.merge_range('D11:E11', '', text2)
      sheet.merge_range('F11:G11', '' , text2)
      sheet.merge_range('D12:E12', '', text2)
      sheet.merge_range('F12:G12', '' , text2)

      sheet.write(12, 3, 'L/C NO.', text1)
      sheet.merge_range('E13:G13', '' , text2)

      sheet.write(13, 3, 'HTS CODE', text1)
      sheet.merge_range('E14:G14', lines.hts_code , text2)

      sheet.merge_range('D15:D16', 'TERM.', text1)
      sheet.merge_range('E15:G16', lines.payment_term_id.name , text2)

      sheet.merge_range('D17:G17', 'REMARKS' , text1)
      sheet.merge_range('D18:G22', lines.comment , text3)


      sheet.merge_range('A5:C5', 'CONSIGNED TO: MESSRS.', head3)
      sheet.merge_range('A8:B8', 'BUYER/ IMPORTER OF RECORD:', head4)
      sheet.write(7, 2, 'SHIP TO:', head4)

      sheet.write(8, 0, lines.partner_id.name, head4)
      sheet.write(9, 0, lines.partner_id.street, head4)
      sheet.write(10, 0, lines.partner_id.street2, head4)

      sheet.write(8, 2, lines.ship, head4)
      sheet.write(9, 2, lines.ship2, head4)
      sheet.write(10, 2, lines.ship3, head4)

      head5 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': False,
        'top':1,
        'right':1,
        'align':'center',
        'valign': 'vcenter',
      })

      head6 = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
        'bold': False,
        'bottom':1,
        'right':1,
        'align':'center',
        'valign': 'vcenter',
      })

      sheet.merge_range('A17:B17', 'FEEDER VESSEL', head5)
      sheet.merge_range('A18:B18', lines.feeder_vessel, head6)

      sheet.merge_range('A19:B19', 'OCEAN VESSEL', head5)
      sheet.merge_range('A20:B20', lines.ocean_vessel, head6)

      sheet.merge_range('A21:B21', 'PORT OF DISCHARGE', head5)
      sheet.merge_range('A22:B22', lines.port_discharge, head6)

      sheet.write(16, 2, 'PLACE OF RECEIPT', head5)
      sheet.write(17, 2, lines.place_receipt, head6)

      sheet.write(18, 2, 'PORT OF LOADING', head5)
      sheet.write(19, 2, lines.port_loading, head6)

      sheet.write(20, 2, 'FINAL DESTINATION', head5)
      sheet.write(21, 2, lines.final_destination, head6)





      sheet.write(22, 0, 'MARKS & NOS', format1)
      sheet.merge_range('B23:C23', 'DESCRIPTION OF GOODS', format1)
      sheet.write(22, 3, 'QTY (CTN)', format1)
      sheet.merge_range('E23:F23', 'PRICE USD/CTN', format1)
      sheet.write(22, 6, 'AMOUNT', format1)
      # sheet.write(23, 0, lines.number , format1)


      i = 23
      no = 0

      obj = self.env['account.invoice.line'].search([('invoice_id','=',lines.id)])
      for obj2 in obj:

        i= i+1
        no=no+1
        sheet.write(i, 0, no, format3)
        sheet.write(i, 1, obj2.product_id.default_code, format3)
        sheet.write(i, 2, obj2.product_id.name, format2)
        sheet.write(i, 3, obj2.quantity, format3)
        sheet.write(i, 4, obj2.price_unit, format3)
        sheet.write(i, 6, obj2.price_subtotal, format3)

      i = i + 2
      sheet.write(i,0, '', format5)
      sheet.write(i,1, '', format5)
      sheet.write(i,2, 'GRAND TOTAL', format5)
      sheet.write(i,3, ' ' , format1)
      sheet.write(i,4, '', format5)
      sheet.write(i,5, '', format5)
      sheet.write(i,6, lines.amount_total , format1)

      i = i + 2
      sheet.write(i, 1, '"NO WOOD PACKAGING MATERIAL"', format6)
      i = i + 2
      sheet.write(i, 1, 'CTN DIMENSION : 340X250X250MM ', format2)
      i = i + 1
      sheet.write(i, 1, 'PACKAGING : 100 PCS/BOX, 10 BOXES/CASE ITEM ', format2)
      i = i + 1
      sheet.write(i, 1, 'TOTAL GROSS WEIGHT: 17,901.82 KGS ', format2)
      i = i + 1
      sheet.write(i, 1, 'TOTAL NETT WEIGHT: 14,625.54 KGS ', format2)

      i = i + 2
      sheet.write(i, 1, 'FDA 510(K) USA:', format6)
      i = i + 1
      sheet.write(i, 1, 'POWDER FREE NITRILE - K 030284 ', format2)

      i = i + 2
      sheet.write(i, 1, 'MEDICAL DEVICE LISTING', format6)
      i = i + 1
      sheet.write(i, 1, 'NITRILE - D 022672 ', format2)
      i = i + 1
      sheet.write(i, 1, 'REGISTRATION NO - 3003591836', format6)

      i = i + 2
      sheet.write(i, 1, 'COUNTRY OF ORIGIN: INDONESIA', format6)

      i = i + 2
      sheet.write(i, 1, 'PLS PAYABLE TO : PT.SMART GLOVE INDONESIA', format6)
      sheet.write(i, 0, 'CONTAINER NO.', format6)
      i = i + 1
      sheet.write(i, 1, 'BANK NAME : PT. BANK UOB INDONESIA', format6)
      sheet.write(i, 0, 'TCNU 6870472', format6)
      i = i + 1
      sheet.write(i, 1, 'JL. Ir.H. DJUANDA NO.20i, KEL. SUKADAMAI,', format6)
      sheet.write(i, 0, 'SEAL NO.', format6)
      i = i + 1
      sheet.write(i, 1, 'KEC. MEDAN POLONIA, KOTA MEDAN ', format6)
      sheet.write(i, 0, 'ID217148A.', format6)
      i = i + 1
      sheet.write(i, 1, 'BENEFICIARY ACCOUNT NO (USD): 396-900-406-0  ', format6)

      i = i + 1
      sheet.write(i, 1, 'SWIFT CODE : BBIJIDJA ', format6)


      border = workbook.add_format({
        'bottom':1,
      })
      i = i + 1
      sheet.write(i, 0, '', border)
      sheet.write(i, 1, '', border)
      sheet.write(i, 2, '', border)
      sheet.write(i, 3, '', border)
      sheet.write(i, 4, '', border)
      sheet.write(i, 5, '', border)
      sheet.write(i, 6, '', border)

      note = workbook.add_format({
        'font_name':'Times', 
        'font_size': 10, 
      })

      ttd = workbook.add_format({
        'font_name':'Times', 
        'bold': True,
        'align': 'center', 
      })


      i = i + 1
      sheet.write(i, 5, 'PT. SMART GLOVE INDONESIA', ttd)

      i = i + 1
      sheet.write(i, 0, '"Interest at the rate of 1.5% per month is chargeable for any invoiced amount not paid in accordance with the"', note)
      i = i + 1
      sheet.write(i, 0, '"agreed payment terms from its due date to the date of payment"', note)

      i = i + 1
      
      sheet.write(i, 4, '', border)
      sheet.write(i, 5, '', border)
      sheet.write(i, 6, '', border)

      i = i + 1    
      sheet.write(i, 5, 'AUTHORISED SIGNATORY', border)