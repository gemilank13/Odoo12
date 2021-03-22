import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class InheritStockCard(models.TransientModel):
    _inherit='stock.card.report.wizard'

    @api.multi
    def button_export_xlsx_v2(self):
        self.ensure_one()
        report_type = 'xlsx'
        return self._export(report_type)


        


