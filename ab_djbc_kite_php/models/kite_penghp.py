import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCKitePenghp(models.Model):
    _name = 'djbc.kite_penghp'
    _description = 'DJBC Pengeluaran Hasil Produksi'

    no_peb = fields.Char (string='No Peb')
    tgl_peb = fields.Char (string='Tgl Peb')
    no_pengeluaran = fields.Char (string='No Pengeluaran')
    tgl_pengeluaran =fields.Date(string='Tgl Pengeluaran')
    pembeli = fields.Char (string='Pembeli')
    negara_tujuan = fields.Char (string='Negara Tujuan')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    jumlah = fields.Char(string='Jumlah')
    mata_uang = fields.Char(string='Mata Uang')
    nilai = fields.Char(string='Nilai')
    djbc = fields.Char(string='DJBC')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_kite_penghp(DATE, DATE);
        CREATE OR REPLACE FUNCTION djbc_kite_penghp(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
	v_date_start DATE;
    v_date_end DATE;
	
	csr cursor for
		select dd.no_dok as no_peb,dd.tgl_dok as tgl_peb,s.reference as no_pengeluaran,s.date as tgl_pengeluaran,rp.name as pembeli,rc.name as negara_tujuan,
		tmp.default_code as kode_barang,tmp.name as nama_barang,uom.name as satuan,s.product_uom_qty as jumlah,so.cur as mata_uang,(so.price_unit*s.product_uom_qty) as nilai,s.id,cat.name as djbc from stock_move s

		left join product_product pp on s.product_id=pp.id
		left join product_template tmp on pp.product_tmpl_id=tmp.id
		left join djbc_categs cat on tmp.djbc_category_id=cat.id
		left join stock_location sl on s.location_dest_id=sl.id
		left join uom_uom uom on s.product_uom=uom.id
		left join stock_picking_type spt on s.picking_type_id=spt.id
		left join stock_picking sp on s.picking_id=sp.id
		left join djbc_docs dd on sp.docs_id=dd.id
		left join djbc_doctype ddt on dd.jenis_dok=ddt.id
		left join res_partner rp on sp.partner_id=rp.id
		left join res_country rc on rp.country_id=rc.id
		left join 
		(select sol.id,so.name as invoice,sol.product_id,cur.name as cur,sol.price_unit,sol.qty_delivered,so.procurement_group_id from sale_order_line sol
		left join sale_order so on sol.order_id=so.id
		left join res_currency cur on sol.currency_id=cur.id) so on so.procurement_group_id=s.group_id and s.product_id=so.product_id 

		where spt.name='Delivery Orders' and  sp.docs_id is not null and so.price_unit is not null and
		((s.date_backdating is not null and (s.date_backdating >= date_start and s.date_backdating <= (date_end::DATE + 1))) or
						(s.date_backdating is null and (s.date >= v_date_start and s.date <= (v_date_end::DATE + 1))));
	
		   
BEGIN
	v_date_start = date_start;
    v_date_end = date_end;
	delete from djbc_kite_penghp;
	
	for rec in csr loop
		insert into djbc_kite_penghp (no_peb, tgl_peb, pembeli, negara_tujuan, no_pengeluaran, tgl_pengeluaran, kode_barang,nama_barang, satuan, jumlah, mata_uang, nilai, djbc) 
			values (rec.no_peb, rec.tgl_peb, rec.pembeli, rec.negara_tujuan, rec.no_pengeluaran, rec.tgl_pengeluaran, rec.kode_barang, rec.nama_barang, rec.satuan, rec.jumlah,
			rec.mata_uang, rec.nilai, rec.djbc) ;
	end loop;
		
END;

$BODY$
LANGUAGE plpgsql;
        """)