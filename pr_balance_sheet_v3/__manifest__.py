# -*- coding: utf-8 -*-
{
    'name': 'Report Balance Xls - Filter Currency',
    'version': '12.0.1.0.0',
    'summary': 'Financial Reports Excel v2 using Foreign Currency',
    'description': 'Financial Reports Excel v2 using Foreign Currency',
    'category': 'Extra Tools',
    'author': 'Geger Gemilank - EDI Indonesia',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['accounting_pdf_reports','pr_balance_sheet_v2'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/pr_balance_sheet.xml',
        'wizards/pr_balance_sheet_wiz.xml',
        'views/menu.xml',
        'reports/report.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
