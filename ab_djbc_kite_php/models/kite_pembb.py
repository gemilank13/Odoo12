import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCKitePembb(models.Model):
    _name = 'djbc.kite_pembb'
    _description = 'DJBC Pemakaian Bahan Baku'

    nomor_pengeluaran = fields.Char (string='Nomor Pengeluaran')
    tanggal_pengeluaran =fields.Date(string='Tanggal Pengeluaran')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    # jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    jumlah_disubkon = fields.Char(string='Jumlah Disubkon')
    jumlah_digunakan = fields.Char(string='Jumlah Digunakan')
    penerima_subkon = fields.Char(string='Penerima Subkon')
    djbc = fields.Char(string='DJBC')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_kite_pembb(DATE, DATE);
        CREATE OR REPLACE FUNCTION djbc_kite_pembb(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
	
	csr cursor for
		select s.reference as nomor_pengeluaran,s.date as tanggal_pengeluaran,tmp.default_code as kode_barang,tmp.name as nama_barang,
        uom.name as satuan,s.product_uom_qty as jumlah_digunakan,0.00 as jumlah_disubkon, '' as penerima_subkon,cat.name as djbc
        from stock_move s
        left join product_product pp on s.product_id=pp.id
        left join product_template tmp on pp.product_tmpl_id=tmp.id
        left join uom_uom uom on s.product_uom=uom.id
        left join djbc_categs cat on tmp.djbc_category_id=cat.id
        left join stock_picking p on s.picking_id=p.id
        left join stock_picking_type spt on p.picking_type_id=spt.id

        where cat.name LIKE '%BAHAN BAKU%' and 
        ((spt.name='Adjustment Out' or spt.name='Delivery Orders' or spt.name='Pemusnahan' or spt.name='Pengrusakan' or spt.name='Pemakaian Bahan Konsumsi') or 
        s.raw_material_production_id is not null or s.consume_unbuild_id is not null) and
        ((s.date_backdating is not null and (s.date_backdating >= '2021-01-01' and s.date_backdating <= ('2021-05-31'::DATE + 1))) or
                        (s.date_backdating is null and (s.date >= '2021-01-01' and s.date <= ('2021-05-31'::DATE + 1))));
	
		   
BEGIN
	delete from djbc_kite_pembb;
	
	for rec in csr loop
		insert into djbc_kite_pembb (nomor_pengeluaran, tanggal_pengeluaran, kode_barang,nama_barang, satuan, jumlah_digunakan, jumlah_disubkon, penerima_subkon, djbc) 
			values (rec.nomor_pengeluaran, rec.tanggal_pengeluaran,rec.kode_barang, rec.nama_barang, rec.satuan, rec.jumlah_digunakan, rec.jumlah_disubkon, rec.penerima_subkon, rec.djbc) ;
	end loop;
		
END;

$BODY$
LANGUAGE plpgsql;
        """)

    # def get_nopen(self):
    #    _logger.info("get_nopen functions...")
    #    for line_id in self.masuk_lines_ids:
    #        _logger.info(line_id.name)
    #        sp_id = self.env['stock.picking'].search([('name','=',line_id.name)])
    #        dok_bc = sp_id.docs_id.read(['no_dok','tgl_dok','jenis_dok'])
    #        if not dok_bc:
    #            _logger.info('dok_bc is empty')
    #        else:
    #            _logger.info(dok_bc[0]['no_dok'])
    #            line_id.write({'no_dok':dok_bc[0]['no_dok'],'tgl_dok':dok_bc[0]['tgl_dok'],'jenis_dok':dok_bc[0]['jenis_dok']})

    # def call_djbc_nofas_masuk(self):
    #    cr = self.env.cr
    #    cr.execute("select djbc_nofas_masuk()")
    #    return {
    #        'name': 'Laporan Pemasukan',
    #        'domain': [],
    #        'view_type': 'form',
    #        'res_model': 'djbc.nofas_masuk',
    #        'view_id': False,
    #        'view_mode': 'tree,form',
    #        'type': 'ir.actions.act_window',
    #    }
