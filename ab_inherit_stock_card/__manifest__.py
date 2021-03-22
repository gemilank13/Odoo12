# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Inherit Stock Card',
    'summary': 'Penambahan field untuk kebutuhan report stock card',
    'version': '12.0.1.0.0',
    'category': '-',
    'website': '-',
    'author': 'Geger - EDI Indonesia',
    'license': 'AGPL-3',
    'depends': [
        'mrp','stock'
    ],
    'data': [
        'views/inherit_mrp.xml',
        # 'views/inherit_inventory.xml',
        'views/inherit_move.xml',
    ],
    'installable': True,
}
