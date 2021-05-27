# -*- coding: utf-8 -*-
{
    'name': 'Laporan Posisi XLSX',
    'version': '12.0.1.0.0',
    'summary': 'Cetakan Laporan Posisi',
    'description': 'Cetakan Laporan Posisi',
    'category': 'Extra Tools',
    'author': 'Geger Gemilank - EDI Indonesia',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['report_xlsx','djbc','djbc_posisi_wip','djbc_nofas_posisi'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
        # 'views/pr_balance_sheet.xml',
        'wizards/inherit_lap_posisi_wip.xml',
        'wizards/inherit_lap_posisi.xml',
        # 'views/menu.xml',
        'reports/report.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
