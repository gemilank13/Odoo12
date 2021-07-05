import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCKitePhp(models.Model):
    _name = 'djbc.kite_pbb'
    _description = 'DJBC Pemasukan Bahan Baku'

    jenis_dok = fields.Char (string='Jenis Dok')
    no_penerimaan = fields.Char (string='No Penerimaan')
    tgl_penerimaan =fields.Date(string='Tgl Penerimaan')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    jumlah = fields.Float(string='Jumlah')
    nilai = fields.Float(string='Nilai')
    satuan = fields.Char(string='Satuan')
    gudang = fields.Char(string='Gudang')
    negara_asal = fields.Char(string='Negara Asal')
    penerima_subkon = fields.Char(string='Penerima Subkon')
    djbc = fields.Char(string='DJBC')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_kite_pbb(DATE, DATE);
        CREATE OR REPLACE FUNCTION djbc_kite_pbb(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
    v_date_start DATE;
    v_date_end DATE;
	
	csr cursor for
		select ddt.code as jenis_dok,dd.no_dok,dd.tgl_dok,s.reference as no_penerimaan,s.date as tgl_penerimaan,tmp.default_code as kode_barang,
        tmp.name as nama_barang,uom.name as satuan,s.product_uom_qty as jumlah,po.cur,po.price_subtotal as nilai,sl.name as gudang, 
        '' as penerima_subkon,rc.name as negara_asal,s.id,cat.name as djbc from stock_move s

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
        (select pl.id,po.name as po,pl.product_id,cur.name as cur,pl.price_subtotal,pl.qty_received,po.group_id from purchase_order_line pl 
        left join purchase_order po on pl.order_id=po.id
        left join res_currency cur on po.currency_id=cur.id) po on po.group_id=s.group_id and s.product_id=po.product_id and s.product_uom_qty=po.qty_received

        where spt.name='Receipts' and  sp.docs_id is not null and
        ((s.date_backdating is not null and (s.date_backdating >= date_start and s.date_backdating <= (date_end::DATE + 1))) or
                                (s.date_backdating is null and (s.date >= v_date_start and s.date <= (v_date_end::DATE + 1))));
	
	
		   
BEGIN
    v_date_start = date_start;
    v_date_end = date_end;
	delete from djbc_kite_pbb;
	
	for rec in csr loop
		insert into djbc_kite_pbb (jenis_dok, no_penerimaan, tgl_penerimaan, kode_barang, nama_barang, satuan, jumlah, nilai, gudang, penerima_subkon, negara_asal, djbc) 
			values (rec.jenis_dok, rec.no_penerimaan, rec.tgl_penerimaan, rec.kode_barang, rec.nama_barang, rec.satuan, rec.jumlah, rec.nilai, rec.gudang, rec.penerima_subkon, 
            rec.negara_asal, rec.djbc) ;
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
