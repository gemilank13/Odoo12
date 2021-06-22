# -*- coding: utf-8 -*-
{
    'name': 'Smart Glove - Invoice Excel',
    'version': '12.0.1.0.0',
    'summary': 'Invoice Excel',
    'description': 'Invoice Excel',
    'category': 'Extra Tools',
    'author': 'Geger Gemilank - PT EDI Indonesia',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['report_xlsx', 'account'],
    'data': [
        'reports/report_xls.xml',
        'views/inherit_invoice.xml',
        # 'wizards/pr_balance_sheet_wiz.xml',
        # 'views/menu.xml',
        # 'reports/report.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
