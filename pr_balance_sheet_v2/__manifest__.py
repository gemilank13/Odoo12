# -*- coding: utf-8 -*-
{
    'name': 'Financial Reports Excel v2',
    'version': '13.0.1.0.0',
    'summary': 'Financial Reports Excel v2 using Foreign Currency',
    'description': 'Financial Reports Excel v2 using Foreign Currency',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['accounting_pdf_reports'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
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
