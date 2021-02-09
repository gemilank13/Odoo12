    # -*- coding: utf-8 -*-
##############################################################################
#
#    Alphasoft Solusi Integrasi, PT
#    Copyright (C) 2014 Alphasoft (<https://www.alphasoft.co.id/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
from odoo.osv.orm import browse_record

ADDRESS_FIELDS = ('street', 'street2', 'rt', 'rw', 'kelurahan_id', 'kecamatan_id', 'kabupaten_id', 'zip', 'city', 'state_id', 'country_id')

class res_partner(models.Model):
    _inherit = 'res.partner'
    _description = 'res partner'
    
    blok = fields.Char('Blok', size=8)
    nomor = fields.Char('Nomor', size=8)
    rt = fields.Char('RT', size=3)
    rw = fields.Char('RW', size=3)
    kelurahan_id = fields.Many2one('res.kelurahan', string="Kelurahan")
    kecamatan_id = fields.Many2one('res.kecamatan', string="Kecamatan")
    kabupaten_id = fields.Many2one('res.kabupaten', string="Kabupaten")
    
    @api.multi
    def _display_address(self, without_company=False):

        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the res.partner to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''
        # get the information that will be injected into the display format
        # get the address format
        address_format = self.country_id.address_format or \
              "%(street)s\n%(street2)s %(blok)s%(nomor)s %(rt)s/%(rw)s\nKel. %(kelurahan_name)s, Kec. %(kecamatan_name)s, Kab. %(kabupaten_name)s\n%(city)s - %(state_name)s %(zip)s\n%(country_name)s"
        args = {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
            'company_name': self.commercial_company_name or '',
            'blok': self.blok and 'Blok.'+ self.blok +'/' or '',
            'nomor': self.nomor and 'No.'+ self.nomor or '',
            'rt': self.rt and 'RT:'+ self.rt +'/' or '',
            'rw': self.rw and 'RW:'+ self.rw or '',
            'kabupaten_name': self.kabupaten_id.name or '',
            'kecamatan_name': self.kecamatan_id.name or '',
            'kelurahan_name': self.kelurahan_id.name or '',
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        if without_company:
            args['company_name'] = ''
        elif self.commercial_company_name:
            address_format = '%(company_name)s\n' + address_format
        #print ('---address_format % args--',address_format,args)
        return address_format % args
    
#     @api.onchange('zip')
#     def onchange_zip(self):
#         if not self.zip:
#             self.kabupaten_id = False
#             self.kecamatan_id = False
#             self.kelurahan_id = False
#             self.city = False
#             self.state_id = False
#             self.country_id = False
#             return
#         if self.zip:
#             kelurahan_obj = self.env['res.kelurahan']
#             kelurahan_id = kelurahan_obj.search([('zip','=',self.zip)])
#             if kelurahan_id:
#                 if len(kelurahan_id) == 1:
#                     kelurahan = kelurahan_id
#                 else:
#                     kelurahan = kelurahan_id[0]
#                 if kelurahan:
#                     self.kelurahan_id = kelurahan.id
#                 if kelurahan.kecamatan_id:
#                     self.kecamatan_id = kelurahan.kecamatan_id.id
#                 if kelurahan.kabupaten_id:
#                     self.kabupaten_id = kelurahan.kabupaten_id.id
#                     self.city = kelurahan.kabupaten_id.name
#                 if kelurahan.kabupaten_id and kelurahan.kabupaten_id.state_id:
#                     self.state_id = kelurahan.kabupaten_id.state_id.id
#                 if kelurahan.kabupaten_id and kelurahan.kabupaten_id.state_id and kelurahan.kabupaten_id.state_id.country_id:
#                     self.country_id = kelurahan.kabupaten_id.state_id.country_id.id
                     
#     @api.onchange('kelurahan_id')
#     def onchange_kelurahan_id(self):
#         if not self.kelurahan_id:
#             self.kabupaten_id = False
#             self.kecamatan_id = False
#             self.zip = False
#             self.city = False
#             self.state_id = False
#             self.country_id = False
#             return
#         if self.kelurahan_id:
#             if self.kelurahan_id.kecamatan_id:
#                 self.kecamatan_id = self.kelurahan_id.kecamatan_id.id
#             if self.kelurahan_id.kabupaten_id:
#                 self.kabupaten_id = self.kelurahan_id.kabupaten_id.id
#                 self.city = self.kelurahan_id.kabupaten_id.name
#             if self.kelurahan_id.kabupaten_id and self.kelurahan_id.kabupaten_id.state_id:
#                 self.state_id = self.kelurahan_id.kabupaten_id.state_id.id
#             if self.kelurahan_id.kabupaten_id and self.kelurahan_id.kabupaten_id.state_id and self.kelurahan_id.kabupaten_id.state_id.country_id:
#                 self.country_id = self.kelurahan_id.kabupaten_id.state_id.country_id.id
#             if self.kelurahan_id.zip:
#                 self.zip = self.kelurahan_id.zip
                
#     @api.onchange('zip', 'kelurahan_id', 'kecamatan_id', 'kabupaten_id')
#     def onchange_localization(self):
#         if self.kabupaten_id:
#             if self.kabupaten_id.state_id:
#                 self.state_id = self.kabupaten_id.state_id.id or False
#             if self.kabupaten_id.state_id and self.kabupaten_id.state_id.country_id:
#                 self.country_id = self.kabupaten_id.state_id.country_id.id
#         elif self.kecamatan_id:
#             if self.kecamatan_id.kabupaten_id:
#                 self.kabupaten_id = self.kecamatan_id.kabupaten_id.id
#                 self.city = self.kecamatan_id.kabupaten_id.name
#             if self.kecamatan_id.kabupaten_id and self.kecamatan_id.kabupaten_id.state_id:
#                 self.state_id = self.kecamatan_id.kabupaten_id.state_id.id
#             if self.kecamatan_id.kabupaten_id and self.kecamatan_id.kabupaten_id.state_id and self.kecamatan_id.kabupaten_id.state_id.country_id:
#                 self.country_id = self.kecamatan_id.kabupaten_id.state_id.country_id.id
#         elif self.kelurahan_id:
#             if self.kelurahan_id.kecamatan_id:
#                 self.kecamatan_id = self.kelurahan_id.kecamatan_id.id
#             if self.kelurahan_id.kabupaten_id:
#                 self.kabupaten_id = self.kelurahan_id.kabupaten_id.id
#                 self.city = self.kelurahan_id.kabupaten_id.name
#             if self.kelurahan_id.kabupaten_id and self.kelurahan_id.kabupaten_id.state_id:
#                 self.state_id = self.kelurahan_id.kabupaten_id.state_id.id
#             if self.kelurahan_id.kabupaten_id and self.kelurahan_id.kabupaten_id.state_id and self.kelurahan_id.kabupaten_id.state_id.country_id:
#                 self.country_id = self.kelurahan_id.kabupaten_id.state_id.country_id.id
#             if self.kelurahan_id.zip:
#                 self.zip = self.kelurahan_id.zip
#         elif self.zip:
#             kelurahan_obj = self.env['res.kelurahan']
#             kelurahan_id = kelurahan_obj.search([('zip','=',self.zip)])
#             if kelurahan_id:
#                 if len(kelurahan_id) == 1:
#                     kelurahan = kelurahan_id
#                 else:
#                     kelurahan = kelurahan_id[0]
#                 if kelurahan:
#                     self.kelurahan_id = kelurahan.id
#                 if kelurahan.kecamatan_id:
#                     self.kecamatan_id = kelurahan.kecamatan_id.id
#                 if kelurahan.kabupaten_id:
#                     self.kabupaten_id = kelurahan.kabupaten_id.id
#                     self.city = kelurahan.kabupaten_id.name
#                 if kelurahan.kabupaten_id and kelurahan.kabupaten_id.state_id:
#                     self.state_id = kelurahan.kabupaten_id.state_id.id
#                 if kelurahan.kabupaten_id and kelurahan.kabupaten_id.state_id and kelurahan.kabupaten_id.state_id.country_id:
#                     self.country_id = kelurahan.kabupaten_id.state_id.country_id.id