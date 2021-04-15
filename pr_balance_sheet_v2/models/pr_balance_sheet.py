from odoo import models, fields, api

class PRBalanceSheet(models.Model):
    _name='pr.balance_sheet'
    _description='Balance Sheet'

    tgl_mulai = fields.Date (string='Date Start')
    tgl_akhir = fields.Date (string='Date End')
    root_type = fields.Char (string='Root Type')
    view_type = fields.Char (string='View Type')
    sub_view_type = fields.Char (string='Sub View Type')	
    account_type = fields.Char (string='Account Type') 
    code=fields.Char (string='Account Code')
    name=fields.Char (string='Account Name')
    cur_period=fields.Float(string='Current Period')
    prev_period=fields.Float(string='Previous Period')
    currency=fields.Char(string='Currency')
    ori_cur_period=fields.Float(string='Original Current Period')
    ori_prev_period=fields.Float(string='Original Previous Period')

    
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS pr_balance_sheet(date, date, date,date);
        CREATE OR REPLACE FUNCTION pr_balance_sheet(date_start date, date_end date, 
		date_start2 date, date_end2 date)
RETURNS VOID AS $BODY$

DECLARE
	x_cur_period float;
	x_ori_cur_period float;	
	x_prev_period float;
	x_ori_prev_period float;
	x_root_type varchar;
	x_view_type varchar;
	x_sub_view_type varchar;

	-- tot_cur_period float;
	-- tot_prev_period float;
	
	csr_kas CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Bank and Cash' or t5.name = 'Credit Card'); 
	csr_piutang CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Receivable');
 
	csr_aktiva_lancar CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Current Assets' or t5.name='Prepayments');

	csr_equivalents CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Cash & Cash equivalents');

	csr_otherreceivable CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Receivable');

	csr_prepaidtax CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Prepaid Tax');

	csr_inventorysm CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Inventory Stock Material');

	csr_inventorysfg CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Inventory Semi Finished Goods');

	csr_inventorys CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Inventory Sparepart');

	csr_oca CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Current Assets');

	csr_aktiva_tidak_lancar CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Non-current Assets');

	csr_other_non_current_assets CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Non Current Assets');

	csr_aktiva_tetap CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Fixed Assets Acquisition');

	csr_acc_dep CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Accumulation Depreciation');

	csr_intang_assets CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Intangible Assets');

	csr_land_assets CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Fixed Assets Land');

	csr_assets_project CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Fixed Assets Project In Progress');
	
	csr_hutang_lancar CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Payable' or t5.name = 'Current Liabilities');

	csr_other_hutang_lancar CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Payable');

	csr_tax_payable CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Tax Payable');

	csr_accrual_deferred CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Accruals And Deferred Income');

	csr_loans CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'S/T Loans');

	csr_provision CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'S/T Provision');

	csr_hutang_jangka_panjang CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Non Current Liabilities');


	csr_lt_loans CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'L/T Loans');

	csr_lt_provision CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'L/T Provision');

	csr_other_non_current_liabilities CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Non Current Liabilities');

	csr_modal CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Equity' or t5.name = 'Current Year Earnings');


	csr_share CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Share & Capital Reserve');

	csr_dividend CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Dividend');

	csr_pl_carried CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Profit/Loss Carried Forward');

	csr_pl_period CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Profit/Loss Of Period');

	csr_other_equity CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Equity Component');



	csr_pendapatan CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Income');

	csr_hpp CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Cost of Revenue' or t5.name = 'Revenue');

	csr_material_cost CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Material Cost');

	csr_direct_cost CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Direct Labor Cost');

	csr_indirect_cost CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Indirect Labor Cost');

	csr_transportation CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Transportation');

	csr_energy_production CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Energy Production');

	csr_maintenance CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Maintenance');

	csr_other_overhead CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Overhead');

	csr_beban_adm CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Expenses' or t5.name = 'Depreciation');

	csr_amortization CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Amortization');

	csr_personel_expenses CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Admin Personel Expenses');

	csr_facility_expenses CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Facility Expenses');

	csr_vehicle_expenses CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Vehicle Expenses');

	csr_it_expenses CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'IT Expenses');

	csr_general_admin_expenses CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'General Admin Expenses');

	csr_pendapatan_lain CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Income' or t5.name = 'Interest Income');

	csr_pce CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Profits on Currency Exchange');

	csr_noi CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Non Operating Income');

	csr_ei CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Extraordinary Income');


	csr_beban_lain CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Expenses' or t5.name = 'Interest Expenses');

	csr_lce CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Loss on Currency Exchange');

	csr_noe CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Non Operating Expenses');

	csr_ee CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Extraordinary Expenses');

	csr_taxes CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Taxes');
   

BEGIN

	delete from pr_balance_sheet;
	
	raise notice 'Aktiva - Kas dan Setara Kas';
	
	raise notice 'start loop';

	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Kas dan Setara Kas';

	for rec in csr_kas loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
                join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted' 
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
                join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	    insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);

	end loop;
	
	
	
	----- START PIUTANG USAHA
	 
	
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Piutang';

	for rec in csr_piutang loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START EQUIVALENTS
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Equivalents';

	for rec in csr_equivalents loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START OTHER RECEIVABLE
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Other Receivable';

	for rec in csr_otherreceivable loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START INVENTORY SM
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Inventory Stock Material';

	for rec in csr_inventorysm loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START INVENTORY SFG
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Inventory';

	for rec in csr_inventorysfg loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START INVENTORY SPAREPART
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Inventory';

	for rec in csr_inventorys loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START OTHER CURRENT ASSETS
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'OTHER CURRENT ASSETS';

	for rec in csr_oca loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START PREPAID TAX
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Prepaid Tax';

	for rec in csr_prepaidtax loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
 		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	
	
        ----- START AKTIVA LANCAR
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Aktiva Lancar';

	for rec in csr_aktiva_lancar loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted' 
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id		
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

   
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

	

 ----- START AKTIVA TIDAK LANCAR
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Aktiva Tidak Lancar';

	for rec in csr_aktiva_tidak_lancar loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted' 
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


 ----- START Other Non Current Assets
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Aktiva Tidak Lancar';

	for rec in csr_other_non_current_assets loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted' 
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	
	
	----- START AKTIVA TETAP
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Aktiva Tetap';

	for rec in csr_aktiva_tetap loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START Accumulation Depreciation
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Accumulation Depreciation';

	for rec in csr_acc_dep loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START Intangible Assets
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Intangible Assets';

	for rec in csr_intang_assets loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	

		----- START Fixed Assets Land
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Fixed Assets Land';

	for rec in csr_land_assets loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	

	----- START Fixed Assets Project
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Fixed Assets Project in Progress';

	for rec in csr_assets_project loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	


	----- START HUTANG LANCAR
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Hutang Lancar';

	for rec in csr_hutang_lancar loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START Other HUTANG LANCAR
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Hutang Lancar';

	for rec in csr_other_hutang_lancar loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START Tax Payable
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Tax Payable';

	for rec in csr_tax_payable loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	

	----- START Accruals And Deferred Income
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Accruals And Deferred Income';

	for rec in csr_accrual_deferred loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START S/T Loans
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'S/T Loans';

	for rec in csr_loans loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START S/T Provision
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'S/T Provision';

	for rec in csr_provision loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START HUTANG JANGKA PANJANG
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Hutang Jangka Panjang';

	for rec in csr_hutang_jangka_panjang loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START L/T LOANS
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Hutang Jangka Panjang';

	for rec in csr_lt_loans loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START L/T Provision
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Hutang Jangka Panjang';

	for rec in csr_lt_provision loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START OTHER NON CURRENT LIABILITIES
	 
	
	x_root_type = 'Balance Sheet';
	x_view_type = 'Hutang';
	x_sub_view_type = 'Hutang Jangka Panjang';

	for rec in csr_other_non_current_liabilities loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	

----- START MODAL
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Modal';
	x_sub_view_type = 'Modal';

	for rec in csr_modal loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START SHARE CAPITAL
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Modal';
	x_sub_view_type = 'Modal';

	for rec in csr_share loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START DIVIDEND
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Modal';
	x_sub_view_type = 'Modal';

	for rec in csr_dividend loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START PL CARRIED
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Modal';
	x_sub_view_type = 'Modal';

	for rec in csr_pl_carried loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START PL PERIOD
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Modal';
	x_sub_view_type = 'Modal';

	for rec in csr_pl_period loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START OTHER EQUITY
	 
	x_root_type = 'Balance Sheet';
	x_view_type = 'Modal';
	x_sub_view_type = 'Modal';

	for rec in csr_other_equity loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START PENDAPATAN
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Pendapatan';
	x_sub_view_type = 'Pendapatan';

	for rec in csr_pendapatan loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	

----- START HPP
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'HPP';
	x_sub_view_type = 'HPP';

	for rec in csr_hpp loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START MATERIAL COST
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Cost of Production';
	x_sub_view_type = 'Material Cost';

	for rec in csr_material_cost loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START DIRECT LABOR COST
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Cost of Production';
	x_sub_view_type = 'Direct Labor Cost';

	for rec in csr_direct_cost loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Indirect Labor Cost
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Cost of Production';
	x_sub_view_type = 'Indirect Labor Cost';

	for rec in csr_indirect_cost loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START TRANSPORTATION
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Cost of Production';
	x_sub_view_type = 'Transportation';

	for rec in csr_transportation loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

----- START Energy Production
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Cost of Production';
	x_sub_view_type = 'Energy Production';

	for rec in csr_energy_production loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Maintenance
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Cost of Production';
	x_sub_view_type = 'Maintenance';

	for rec in csr_maintenance loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

----- START Other Overhead
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Cost of Production';
	x_sub_view_type = 'Other Overhead';

	for rec in csr_other_overhead loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	
----- START BEBAN ADMINISTRASI DAN UMUM
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Adm dan Umum';
	x_sub_view_type = 'Beban Adm dan Umum';

	for rec in csr_beban_adm loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

----- START Amortization
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Adm dan Umum';
	x_sub_view_type = 'Amortization';

	for rec in csr_amortization loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START ADMIN PERSONEL EXPENSES
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Adm dan Umum';
	x_sub_view_type = 'Admin Personel Expenses';

	for rec in csr_personel_expenses loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START FACILITY EXPENSES
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Adm dan Umum';
	x_sub_view_type = 'Beban Adm dan Umum';

	for rec in csr_facility_expenses loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START VEHICLE EXPENSES
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Adm dan Umum';
	x_sub_view_type = 'VEHICLE EXPENSES';

	for rec in csr_vehicle_expenses loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START IT EXPENSES
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Adm dan Umum';
	x_sub_view_type = 'IT Expenses';

	for rec in csr_it_expenses loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

----- START GENERAL ADMIN EXPENSES
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Adm dan Umum';
	x_sub_view_type = 'General Admin Expenses';

	for rec in csr_general_admin_expenses loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START Pendapatan Lain-Lain
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Pendapatan Lain-Lain';
	x_sub_view_type = 'Pendapatan Lain-Lain';

	for rec in csr_pendapatan_lain loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Profits on Currency Exchange
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Pendapatan Lain-Lain';
	x_sub_view_type = 'Profits on Currency Exchange';

	for rec in csr_pce loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START Non Operating Income
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Pendapatan Lain-Lain';
	x_sub_view_type = 'Non Operating Income';

	for rec in csr_noi loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	


----- START Extraordinary Income
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Pendapatan Lain-Lain';
	x_sub_view_type = 'Extraordinary Income';

	for rec in csr_ei loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START Beban Lain-Lain
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Lain-Lain';
	x_sub_view_type = 'Beban Lain-Lain';

	for rec in csr_beban_lain loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START Beban Lain-Lain
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Lain-Lain';
	x_sub_view_type = 'Beban Lain-Lain';

	for rec in csr_lce loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START Beban Lain-Lain
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Lain-Lain';
	x_sub_view_type = 'Beban Lain-Lain';

	for rec in csr_noe loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START Beban Lain-Lain
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Lain-Lain';
	x_sub_view_type = 'Beban Lain-Lain';

	for rec in csr_ee loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START TAXES
	 
	x_root_type = 'Laba/Rugi';
	x_view_type = 'Beban Lain-Lain';
	x_sub_view_type = 'Taxes';

	for rec in csr_taxes loop
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
		into x_cur_period, x_ori_cur_period;
		if x_cur_period is null then
			x_cur_period=0;
		end if;
		if x_ori_cur_period is null then
			x_ori_cur_period=0;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;
	
	    select sum (balance), sum (amount_currency)
		from account_move_line t1
		join account_move t2 on t2.id=t1.move_id
		where t1.account_id = rec.x_id 
		and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
		into x_prev_period, x_ori_prev_period;
		if x_prev_period is null then
			x_prev_period=0;
		end if;
		if x_ori_prev_period is null then
			x_ori_prev_period=0;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;

	    
	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, 
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;
	


	
END;


$BODY$
LANGUAGE plpgsql;
        """
        )
    

