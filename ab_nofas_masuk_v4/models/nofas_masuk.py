import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCNofasMasuk(models.Model):
    _name = 'djbc.nofas_masuk_v4'
    _description = 'DJBC Laporan Pemasukan'
    _rec_name = 'no_dok'

    jenis_dok = fields.Char(string='Jenis Dokumen')
    # no_aju = fields.Char(string='Nomor Aju')
    # tgl_aju=fields.Date(string='Tgl Aju')
    no_dok=fields.Char (string='Nomor Pendaftaran')
    # no_dok  = fields.Many2one(comodel_name="djbc.docs", string="Nomor Pendaftaran", required=False, )
    tgl_dok=fields.Date(string='Tgl Pendaftaran')
    # no_penerimaan = fields.Many2one(comodel_name="stock.picking", string="Nomor Penerimaan", required=False, )
    tgl_penerimaan=fields.Date(string='Tgl Penerimaan')
    # no_bl = fields.Char(string='Nomor B/L')
    # tgl_bl = fields.Date(string='Tgl B/L')
    # no_cont = fields.Char(string='Nomor Container')
    no_penerimaan=fields.Char(string='Nomor Penerimaan')
    pengirim = fields.Char(string='Pengirim Barang')
    # pemilik = fields.Char(string='Pemilik Barang')
    # hs_code = fields.Char(string='HS Code')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    # lot_id = fields.Many2one(comodel_name="stock.production.lot", string="Lot No", required=False, )
    jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    # jumlah_kemasan = fields.Float(string='Jumlah Kemasan')
    # satuan_kemasan = fields.Char(string='Satuan Kemasan') 
    nilai = fields.Float(string='Nilai')
    currency = fields.Char(string='Currency')
    # location = 	fields.Char(string='Location')
    warehouse = fields.Char(string='Warehouse')
    # alm_wh = fields.Char(string='Alamat Warehouse')
    # kota_wh = fields.Char(string='Kota')
    # date_backdating = fields.Date(string='Date Backdating')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_nofas_masuk_v4(DATE, DATE);
        CREATE OR REPLACE FUNCTION djbc_nofas_masuk_v4(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
	
	csr cursor for
		SELECT doc.code as jenis_dok,bc.no_dok,bc.tgl_dok,sm.reference as no_penerimaan,
        CASE WHEN sm.date_backdating IS NULL THEN sp.date_done ELSE sm.date_backdating END AS tgl_penerimaan
        ,rp.name AS pengirim,pt.default_code as kode_barang,pt.name as nama_barang ,sm.product_uom_qty as jumlah, uom.name AS satuan,
        CASE WHEN aml.price_subtotal IS NULL THEN inv.price_subtotal ELSE aml.price_subtotal END AS nilai,
        CASE WHEN cur.name IS NULL THEN inv.name ELSE cur.name END AS currency
        ,(SELECT code FROM stock_warehouse WHERE partner_id=1) AS warehouse
        --,aml.name AS PO,sm.name,spt.name 
        FROM stock_move sm
        LEFT JOIN stock_picking_type spt ON sm.picking_type_id=spt.id
        LEFT JOIN product_product p ON sm.product_id=p.id
        LEFT JOIN product_template pt ON p.product_tmpl_id=pt.id
        LEFT JOIN uom_uom uom ON sm.product_uom=uom.id
        --LEFT JOIN purchase_order_line pol ON sm.purchase_line_id=pol.id
        --LEFT JOIN (SELECT * FROM account_invoice_line aml LEFT JOIN purchase_order_line pol ON aml.purchase_line_id=pol.id) inv ON inv.purchase_line_id=sm.purchase_line_id
        LEFT JOIN  account_invoice_line aml ON aml.purchase_line_id=sm.purchase_line_id
        LEFT JOIN res_currency cur ON aml.currency_id=cur.id
        LEFT JOIN (SELECT rel.move_id,al.id,al.price_subtotal,cur.name FROM stock_move_invoice_line_rel rel
                            LEFT JOIN account_invoice_line al ON rel.invoice_line_id=al.id
                            LEFT JOIN res_currency cur ON al.currency_id=cur.id) inv ON sm.id=inv.move_id
        LEFT JOIN stock_picking sp ON sm.picking_id=sp.id   
        LEFT JOIN res_partner rp ON sp.partner_id=rp.id
        LEFT JOIN djbc_docs bc ON sp.docs_id=bc.id
        LEFT JOIN djbc_doctype doc ON bc.jenis_dok=doc.id
        WHERE spt.code='incoming' and sp.docs_id IS NOT NULL and sp.state='done';
	
	v_wh text;
		   
BEGIN
	delete from djbc_nofas_masuk_v4;
	-- v_wh='WH/Stock';
	
	for rec in csr loop
		insert into djbc_nofas_masuk_v4 (no_dok, tgl_dok,jenis_dok,no_penerimaan, tgl_penerimaan, pengirim, kode_barang,
			nama_barang, jumlah, satuan, nilai, currency, warehouse) 
			values (rec.no_dok, rec.tgl_dok, rec.jenis_dok, rec.no_penerimaan, rec.tgl_penerimaan,
				rec.pengirim, rec.kode_barang, rec.nama_barang, rec.jumlah, rec.satuan, 
				rec.nilai, rec.currency, rec.warehouse) ;
		-- update stock_move set djbc_masuk_flag=TRUE where id=rec.id;
	end loop;
		
END;

$BODY$
LANGUAGE plpgsql;
        """)
