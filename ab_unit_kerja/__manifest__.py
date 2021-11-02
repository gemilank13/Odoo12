# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'EDI Indonesia - Inherit Unit Kerja - PMP',
    'summary': 'Penambahan field unit kerja',
    'version': '12.0.1.0.0',
    'category': '-',
    'website': '-',
    'author': 'Geger - EDI Indonesia',
    'license': 'AGPL-3',
    'depends': [
        'base','product','account','purchase'
    ],
    'data': [
        'views/inherit_user.xml',
        'views/inherit_barang.xml',
        'views/inherit_vendor_bill.xml',
        'views/inherit_invoice.xml',
        'views/inherit_journal.xml',
        'views/inherit_journal_item.xml',
        'views/inherit_invoice_line.xml',

    ],
    'installable': True,
}
