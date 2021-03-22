# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Inherit Stock Card Report',
    'summary': 'Custom Report Stock Card',
    'version': '12.0.1.0.0',
    'category': 'Warehouse',
    'website': '---',
    'author': 'Geger - EDI Indonesia',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'date_range',
        'report_xlsx_helper',
        'stock_card_report'
    ],
    'data': [
        # 'data/paper_format.xml',
        # 'data/report_data.xml',
        'reports/inherit_stock_card_report_wizard.xml',
        # 'wizard/stock_card_report_wizard_view.xml',
    ],
    'installable': True,
}
#
