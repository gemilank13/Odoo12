# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models 
from datetime import datetime 
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    ''' Defining a student information '''
    _inherit = "account.journal"

    type = fields.Selection(selection_add=[
            ('sale_advance', 'Advance Sale'),
            ('purchase_advance', 'Advance Purchase')])
    
class AccountAccount(models.Model):
    _inherit = 'account.account'
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=', name), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        account_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(account_ids).name_get()
    
class AccountInvoice(models.Model):
    ''' Defining a student information '''
    _inherit = "account.invoice"
    
    def _compute_invoice_docs_count(self):
        Attachment = self.env['ir.attachment']
        for task in self:
            task.doc_count = Attachment.search_count([
                ('res_model', '=', 'account.invoice'), ('res_id', '=', task.id)
            ])
            
    @api.multi
    @api.depends('date_due')
    def _get_aged_due(self):
        for invoice in self:
            invoice.aged_due = '0 Days'
            if invoice.date_due and invoice.state != 'paid':
                date_date_from = fields.Date.from_string(fields.Date.today())
                date_date_to = fields.Date.from_string(invoice.date_due)
                date_diff_days = (date_date_to - date_date_from).days
                invoice.aged_due = str(date_diff_days) + ' Day'
    
    doc_count = fields.Integer(compute='_compute_invoice_docs_count', string="Number of documents attached")
    aged_due = fields.Char('Aged fr Due', compute='_get_aged_due', store=False)
    attn = fields.Char('Attention',size=64)
    signature = fields.Char('Signature', size=64)
    journal_bank_id = fields.Many2one('account.journal', string='Payment Method', domain=[('type', 'in', ('cash','bank'))])
    
    
    @api.multi
    def action_invoice_paid(self):
        # lots of duplicate calls to action_invoice_paid, so we remove those already paid
        to_pay_invoices = self.filtered(lambda inv: inv.state != 'paid')
        if to_pay_invoices.filtered(lambda inv: inv.state not in ('open', 'in_payment')):
            raise UserError(_('Invoice must be validated in order to set it to register payment.'))
        if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
            raise UserError(_('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))

        for invoice in to_pay_invoices:
            if any([move.journal_id.post_at_bank_rec and move.state == 'draft' for move in invoice.payment_move_line_ids.mapped('move_id')]):
                invoice.write({'state': 'in_payment'})
            else:
                invoice.write({'state': 'paid'})
            invoice.write({'journal_bank_id': invoice.payment_ids and invoice.payment_ids[0].journal_id.id})
    
    @api.model
    def invoice_line_move_line_get(self):
        """Copy from invoice line to move lines"""
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        ailo = self.env['account.invoice.line']
        for move_line_dict in res:
            if move_line_dict.get('invl_id'):
                iline = ailo.browse(move_line_dict['invl_id'])
                move_line_dict['categ_id'] = iline.categ_id.id
        return res
    
#     @api.depends('partner_id', 'currency_id', 'date_invoice', 'is_currency_set')
#     def _get_currency_rate(self):
#         for invoice in self:
#             company_currency = invoice.company_currency_id
#             invoice_currency = invoice.currency_id or company_currency
#             if invoice_currency != company_currency:
#                 invoice.force_rate = invoice_currency.with_context(partner_id=invoice.partner_id.id,date=invoice.date_invoice).compute(1.0, company_currency, round=False)
#             else:
#                 invoice.force_rate = 1.0

    
    @api.multi
    def attachment_invoice_view(self):
        self.ensure_one()
        domain = [
            ('res_model', '=', 'account.invoice'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the invoice.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your invoice.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }
    
    
    @api.model
    def _cron_send_invoice(self):
        date_now = datetime.now().strftime("%Y-%m-%d")
        current_date = datetime.strptime(date_now,"%Y-%m-%d").date()
        invoices = self.search([('date_due','<=',current_date),('state','=','open'),('type','=','out_invoice')])
        #print ('====_cron_send_invoice==',invoices)
        return invoices._auto_send_invoice()
    
    def _auto_send_invoice(self):
        for invoice in self:
            email_context = self.env.context.copy()
            partners_to_email = [child for child in invoice.partner_id.child_ids if child.type == 'invoice' and child.email]
            #print ('===partners_to_email==',partners_to_email)
            if not partners_to_email and invoice.partner_id.email:
                partners_to_email = [invoice.partner_id]
            #print ('===partners_to_email==',partners_to_email)
            if partners_to_email:            
                email_context.update({
                    'total_amount': invoice.amount_total,
                    'email_to': ','.join([partner.email for partner in partners_to_email]),
                    'number': invoice.number,
                    'currency': invoice.currency_id.name,
                    'date_invoice': invoice.date_invoice,
                    'date_due': invoice.date_due,
                })
                _logger.debug("Sending Invoice Mail to %s", invoice.number)
                print ('====_auto_send_invoice==',email_context)
                mail_template_id = self.env['ir.model.data'].xmlid_to_object('aos_base_account.email_template_account_invoice_due_id')
                mail_template_id.with_context(email_context).send_mail(invoice.id, notif_layout="mail.mail_notification_paynow")
    
class AccountInvoiceLine(models.Model):    
    _inherit = "account.invoice.line"

    categ_id = fields.Many2one('product.category', string="Category", related='product_id.categ_id', store=True)
    
    
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    @api.multi
    @api.depends('line_ids.debit', 'line_ids.credit', 'manual_compute')
    def _amount_compute(self):
        for move in self:
            total = 0.0
            for line in move.line_ids:
                total += line.debit
            move.amount = total
    
    manual_compute = fields.Boolean('Manual Compute')
    product_id = fields.Many2one('product.product', related='line_ids.product_id', string='Product', readonly=False)
    amount = fields.Monetary(compute='_amount_compute', store=True)

    @api.multi
    def _post_validate(self):
        vals = super(AccountMove, self)._post_validate()
        for move in self:
            move.manual_compute = True
        return vals
    
class AccountMoveLine(models.Model):
    ''' Defining a student information '''
    _inherit = "account.move.line"
    
    @api.multi
    @api.depends('date_maturity', 'reconciled')
    def _get_aged_due(self):
        for mline in self:
            mline.aged_due = '0 Days'
            if mline.date_maturity and mline.reconciled:
                date_date_from = fields.Date.from_string(fields.Date.today())
                date_date_to = fields.Date.from_string(mline.date_maturity)
                date_diff_days = (date_date_to - date_date_from).days
                mline.aged_due = str(date_diff_days) + ' Day'
    
    categ_id = fields.Many2one('product.category', string="Category")
    aged_due = fields.Char('Aged fr Due', compute='_get_aged_due', store=True)
    
class ProductProduct(models.Model):
    _inherit = "product.product"

#     def _anglo_saxon_sale_move_lines(self, name, product, uom, qty, price_unit, currency=False, amount_currency=False, fiscal_position=False, account_analytic=False, analytic_tags=False):
#         res = super(ProductProduct, self)._anglo_saxon_sale_move_lines(name=name, product=product, uom=uom, qty=qty, price_unit=price_unit, currency=currency, amount_currency=amount_currency, fiscal_position=fiscal_position, account_analytic=account_analytic, analytic_tags=analytic_tags)
#         #CHANGE NAME COGS N INTERIM OUT WITH ORIGIN
#         if res and self._context.get('line'):
#             res[0]['categ_id'] = self._context.get('line').categ_id or self._context.get('line').categ_id.id or False
#             res[1]['categ_id'] = self._context.get('line').categ_id or self._context.get('line').categ_id.id or False           
#         return res

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        vals = super(ProductProduct, self)._convert_prepared_anglosaxon_line(line=line, partner=partner)
        vals['categ_id'] = line.get('categ_id', False)
        return vals
    
    
# class AccountInvoiceLine(models.Model):
#     _inherit = 'account.invoice.line'
#     
#     def _get_price_tax(self):
#         for l in self:
#             l.price_tax = l.price_total - l.price_subtotal
#     
#     price_tax = fields.Monetary(string='Tax Amount', compute='_get_price_tax', store=False)
    