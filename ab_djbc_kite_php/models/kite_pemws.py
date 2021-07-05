import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCKitePemws(models.Model):
    _name = 'djbc.kite_pemws'
    _description = 'DJBC Pemakaian WIP Subkontrak'

    nomor_pengeluaran = fields.Char (string='Nomor Pengeluaran')
    tanggal_pengeluaran =fields.Date(string='Tanggal Pengeluaran')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    # jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    jumlah_disubkon = fields.Char(string='Jumlah Disubkon')
#     jumlah_digunakan = fields.Char(string='Jumlah Digunakan')
    penerima_subkon = fields.Char(string='Penerima Subkon')
    # djbc = fields.Char(string='DJBC')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_kite_pemws(DATE, DATE);
        CREATE OR REPLACE FUNCTION djbc_kite_pemws(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
	v_date_start DATE;
	v_date_end DATE;
	
	csr cursor for
		select s.reference as nomor_pengeluaran,s.date as tanggal_pengeluaran,tmp.default_code as kode_barang,tmp.name as nama_barang,
		uom.name as satuan,s.product_uom_qty as jumlah_disubkon,rp.name as penerima_subkon
		from stock_move s
		left join product_product pp on s.product_id=pp.id
		left join product_template tmp on pp.product_tmpl_id=tmp.id
		left join uom_uom uom on s.product_uom=uom.id
		left join stock_picking p on s.picking_id=p.id
		left join stock_picking_type spt on p.picking_type_id=spt.id
		left join res_partner rp on p.partner_id=rp.id

		where spt.name='Subkon' and
		((s.date_backdating is not null and (s.date_backdating >= date_start and s.date_backdating <= (date_end::DATE + 1))) or
						(s.date_backdating is null and (s.date >= v_date_start and s.date <= (v_date_end::DATE + 1))));
	
		   
BEGIN
	v_date_start = date_start;
    v_date_end = date_end;
	delete from djbc_kite_pemws;
	
	for rec in csr loop
		insert into djbc_kite_pemws (nomor_pengeluaran, tanggal_pengeluaran, kode_barang,nama_barang, satuan, jumlah_disubkon, penerima_subkon) 
			values (rec.nomor_pengeluaran, rec.tanggal_pengeluaran,rec.kode_barang, rec.nama_barang, rec.satuan, rec.jumlah_disubkon, rec.penerima_subkon) ;
	end loop;
		
END;

$BODY$
LANGUAGE plpgsql;
        """)
