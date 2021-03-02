# -*- coding: utf-8 -*-
{
    'name': 'DJBC Generate XLS',
    'version': '12.0.1.0.0',
    'summary': 'DJBC Generate XLS',
    'description': 'Module Inherit Untuk Generate Excel',
    'category': 'Extra Tools',
    'author': 'Geger Gemilank',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['report_xlsx','djbc','djbc_nofas_masuk_v2','djbc_nofas_keluar_v2'],
    'data': [
  #       'security/ir.model.access.csv',
  #       'views/mutasi.xml',
  		'reports/report.xml',
        'wizards/inherit_pemasukan.xml',
        'wizards/inherit_pengeluaran.xml',
  #       'views/menu.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
