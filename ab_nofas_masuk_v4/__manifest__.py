# -*- coding: utf-8 -*-
{
    'name': 'DJBC Pemasukan V4',
    'version': '12.0.1.0.0',
    'summary': ' ',
    'description': ' ',
    'category': 'Extra Tools',
    'author': 'Geger ',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/nofas_masuk_wiz.xml',
        'views/nofas_masuk.xml',
        'views/menu.xml',
        'reports/report.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
}
