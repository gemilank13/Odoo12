# -*- coding: utf-8 -*-
{
    'name': 'Custom Inventory (WH/IN)',
    'version': '12.0.1.0.0',
    'summary': ' ',
    'description': ' ',
    'category': 'Extra Tools',
    'author': 'Geger Gemilank - PT EDI-INDONESIA',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['stock','base'],
    'data': [
        'views/inherit_inv.xml',
        'views/inherit_stock_move.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
