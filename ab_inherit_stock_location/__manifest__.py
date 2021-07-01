#
# -*- coding: utf-8 -*-
{
    'name': "DJBC Kite Apps",

    'summary': """Laporan IT Inventory DJBC""",
    'description': """    Laporan IT Inventory DJBC untuk fasilitas TPB (KB, PLB, GB), KITE dan Non Fasilitas (Umum). """,
    'author': "Geger Gemilank",
    'website': "-",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['djbc','stock','product','stock_picking_purchase_order_link','stock_picking_sale_order_link','report_xlsx','base'],

    # always loaded
    'data': [
	    'views/stock_location.xml',
	    # 'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application' : True
}
