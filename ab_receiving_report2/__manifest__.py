# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Receivement Report 2',
    'summary': 'Inventory',
    'version': '12.0.1.0.0',
    'category': '-',
    'website': '-',
    'author': 'Geger - EDI Indonesia',
    'license': 'AGPL-3',
    'depends': [
        'stock'
    ],
    'data': [
        'reports/report.xml',
        'wizards/receivement_wiz.xml',
        # 'views/inherit_move.xml',
    ],
    'installable': True,
}
