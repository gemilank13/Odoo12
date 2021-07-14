# -*- coding: utf-8 -*-
{
    'name': 'DJBC Kite Generate XLS',
    'version': '12.0.1.0.0',
    'summary': 'DJBC Kite Generate XLS',
    'description': 'Module Inherit Untuk Generate Excel DJBC Kite',
    'category': 'Extra Tools',
    'author': 'Geger Gemilank',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['report_xlsx','djbc','ab_djbc_kite_php'],
    'data': [
    	'reports/report.xml',
    	'wizards/inherit_kite_mbb.xml',
        'wizards/inherit_kite_mhp.xml',
        'wizards/inherit_kite_pbb.xml',
        'wizards/inherit_kite_pembb.xml',
        'wizards/inherit_kite_pemws.xml',
        'wizards/inherit_kite_penghp.xml',
        'wizards/inherit_kite_php.xml',
        'wizards/inherit_kite_pw.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
