import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCKitePhp(models.Model):
    _name = 'djbc.kite_pw'
    _description = 'DJBC Pemasukan Hasil Produksi'

    nomor = fields.Char (string='Nomor')
    tanggal =fields.Date(string='Tanggal')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    # jumlah_disubkon = fields.Char(string='Jumlah Disubkon')
    gudang = fields.Char(string='Gudang')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_kite_pw(DATE, DATE);
        CREATE OR REPLACE FUNCTION djbc_kite_pw(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
    v_date_start DATE;
    v_date_end DATE;
    
    csr cursor for
        select s.reference as nomor,s.date as tanggal,tmp.default_code as kode_barang,tmp.name as nama_barang,uom.name as satuan,s.product_uom_qty as jumlah,sl.name as gudang, 
        s.id from stock_move s

        left join stock_location sl on s.location_dest_id=sl.id
        left join product_product pp on s.product_id=pp.id
        left join product_template tmp on pp.product_tmpl_id=tmp.id
        left join uom_uom uom on s.product_uom=uom.id

        where sl.is_waste_kite='t' and 
        ((s.date_backdating is not null and (s.date_backdating >= date_start and s.date_backdating <= (date_end::DATE + 1))) or
                        (s.date_backdating is null and (s.date >= v_date_start and s.date <= (v_date_end::DATE + 1))));
    
    
           
BEGIN
    v_date_start = date_start;
    v_date_end = date_end;
    delete from djbc_kite_pw;
    
    for rec in csr loop
        insert into djbc_kite_pw (nomor, tanggal, kode_barang,nama_barang, satuan, jumlah, gudang) 
            values (rec.nomor, rec.tanggal,rec.kode_barang, rec.nama_barang, rec.satuan, rec.jumlah, rec.gudang) ;
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
