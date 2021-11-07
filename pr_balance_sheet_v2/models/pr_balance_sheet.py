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
    group_id = fields.Char (string='Group')
    code=fields.Char (string='Account Code')
    name=fields.Char (string='Account Name')
    cur_period=fields.Float(string='Current Period')
    prev_period=fields.Float(string='Previous Period')
    currency=fields.Char(string='Currency')
    ori_cur_period=fields.Float(string='Original Current Period')
    ori_prev_period=fields.Float(string='Original Previous Period')
    unit_kerja =fields.Char(string='Unit Kerja')


    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS pr_balance_sheet(date, date, date,date,varchar);
        CREATE OR REPLACE FUNCTION pr_balance_sheet(date_start date, date_end date,
		date_start2 date, date_end2 date, unk varchar)
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


	pl_material_third CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Material third') order by x_code asc;

	pl_material_group CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Material group') order by x_code asc;

	pl_tot_material CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Total material costs & energy') order by x_code asc;

	pl_personnel_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Personnel expenses') order by x_code asc;

	pl_sales_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Sales expenses') order by x_code asc;

	pl_transport_log CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Transport & logistics') order by x_code asc;

	pl_advertising_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Advertising expenses') order by x_code asc;

	pl_facility_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Facility expenses') order by x_code asc;

	pl_maintenance CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Maintenance/Repair (excl. facility and vehicles)') order by x_code asc;


	pl_vehicles CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Vehicles') order by x_code asc;

	pl_it_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'IT-Expenses') order by x_code asc;

	pl_admin_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Administration expenses') order by x_code asc;

	pl_licensing CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Licensing') order by x_code asc;

	pl_tot_operating_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Total operating expenses') order by x_code asc;

	pl_depreciation CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Depreciation fixed assets') order by x_code asc;

	pl_amortization CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Amortization on immat. assets') order by x_code asc;


	pl_gs_dom CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Gross sales domestic from goods and services') order by x_code asc;

	pl_gs_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Gross sales export from goods and services') order by x_code asc;


	pl_gs_group CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Gross sales group from goods and services') order by x_code asc;

	pl_gs_rel CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Total revenue deductions from goods and services') order by x_code asc;

	pl_tot_rd CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Gross sales related comp from goods and services') order by x_code asc;

	pl_icf CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Inventory change finished/semi-finished goods') order by x_code asc;

	pl_ooi CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Other operating Income') order by x_code asc;

	pl_ii CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Interest income') order by x_code asc;

	pl_di CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Dividend income') order by x_code asc;


	pl_pfp CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Profit From Participations') order by x_code asc;

	pl_pos CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Profit On Securities') order by x_code asc;

	pl_poce CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Profit On Currency Exchange') order by x_code asc;


	pl_in_ex CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Interest Expenses') order by x_code asc;

	pl_lfp CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Losses From Participations') order by x_code asc;

	pl_los CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Losses On Securities') order by x_code asc;

	pl_loce CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Losses On Currency Exchange') order by x_code asc;

	pl_non_or CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Non-operating result') order by x_code asc;


	pl_er CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Extraordinary result') order by x_code asc;

	pl_icg CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'IC-postings Group') order by x_code asc;

	pl_tax CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Taxes') order by x_code asc;

	pl_mi CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Minority interests') order by x_code asc;



	csr_equivalents CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Cash & cash equivalents') order by x_code asc;

	csr_ar CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Accounts receivables') order by x_code asc;

	csr_or CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Other receivables') order by x_code asc;

	csr_stl CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'S/T loans') order by x_code asc;

	csr_trm CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Tobacco and raw material') order by x_code asc;

	csr_sfg CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Semi finished goods') order by x_code asc;

	csr_ftg CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Finished and trading goods') order by x_code asc;

	csr_peai CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Prepaid expenses and accrued income') order by x_code asc;

	csr_participations CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Participations') order by x_code asc;

	csr_dt CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Deferred taxes') order by x_code asc;

	csr_ltl CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'L/T loans') order by x_code asc;

	csr_mpe CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Machinery&production equipment') order by x_code asc;


	csr_cv CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Cars & vehicles') order by x_code asc;

	csr_ite CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'IT & telecom equipment') order by x_code asc;

	csr_oe CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Office equipment (incl. shop)') order by x_code asc;

	csr_ob CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Operational buildings (incl. land)') order by x_code asc;

	csr_farm CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Farm') order by x_code asc;

	csr_greenhouse CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Greenhouse') order by x_code asc;


	csr_nob CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Non operational buildings') order by x_code asc;

	csr_ia CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Intangible assets') order by x_code asc;

	csr_stlib CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'S/T loans interest bearing') order by x_code asc;

	csr_ap CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Accounts payable') order by x_code asc;

	csr_op CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Other payables (non-interest bearing)') order by x_code asc;

	csr_olib CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Other liabilities interest bearing') order by x_code asc;

	csr_stp CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'S/T provisions') order by x_code asc;

	csr_adi CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Accruals and deferred income') order by x_code asc;

	csr_ltllib CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'L/T loans & liabilities interest bearing') order by x_code asc;

	csr_ltllnib CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'L/T loans & liabilities non-interest bearing') order by x_code asc;

	csr_ltp CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'L/T provisions') order by x_code asc;

	csr_dtl CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Deferred tax liabilities') order by x_code asc;

	csr_tem CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Total equity excl. minority') order by x_code asc;

	csr_temi CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'Total equity incl. minority interests') order by x_code asc;


	csr_bsd CURSOR FOR
		select t1.id as x_id, t1.code as x_code, t1.name x_name, t6.name as x_group,
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join account_group t6 on t1.group_id = t6.id
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id
			where (t5.name = 'BS-Difference') order by x_code asc;




BEGIN

	delete from pr_balance_sheet;

	raise notice 'Aktiva - Kas dan Setara Kas';

	raise notice 'start loop';


----- START EQUIVALENTS


	x_root_type = 'Balance Sheet';
	x_view_type = 'Aktiva';
	x_sub_view_type = 'Balance Sheet';

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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Accounts receivables


	x_root_type = 'Balance Sheet';
	x_view_type = 'Accounts receivables';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ar loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START L/T loans & liabilities interest bearing


	x_root_type = 'Balance Sheet';
	x_view_type = 'L/T loans & liabilities interest bearing';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ltllib loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START BS-Difference


	x_root_type = 'Balance Sheet';
	x_view_type = 'BS-Difference';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_bsd loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START L/T loans & liabilities non-interest bearing


	x_root_type = 'Balance Sheet';
	x_view_type = 'L/T loans & liabilities non-interest bearing';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ltllnib loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START L/T provisions


	x_root_type = 'Balance Sheet';
	x_view_type = 'L/T provisions';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ltp loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Total equity excl. minority


	x_root_type = 'Balance Sheet';
	x_view_type = 'Total equity excl. minority';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_tem loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Total equity excl. minority interests


	x_root_type = 'Balance Sheet';
	x_view_type = 'Total equity excl. minority interests';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_temi loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START Deferred tax liabilities


	x_root_type = 'Balance Sheet';
	x_view_type = 'Deferred tax liabilities';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_dtl loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START Accounts Payable


	x_root_type = 'Balance Sheet';
	x_view_type = 'Accounts payable';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ap loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Other payables (non-interest bearing)


	x_root_type = 'Balance Sheet';
	x_view_type = 'Other payables (non-interest bearing)';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_op loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Other liabilities interest bearing


	x_root_type = 'Balance Sheet';
	x_view_type = 'Other liabilities interest bearing';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_olib loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START S/T provisions


	x_root_type = 'Balance Sheet';
	x_view_type = 'S/T provisions';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_stp loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Accruals and deferred income


	x_root_type = 'Balance Sheet';
	x_view_type = 'Accruals and deferred income';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_adi loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START S/T loans interest bearing


	x_root_type = 'Balance Sheet';
	x_view_type = 'S/T loans interest bearing';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_stlib loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START Intangible assets


	x_root_type = 'Balance Sheet';
	x_view_type = 'Intangible assets';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ia loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Other receivables

	x_root_type = 'Balance Sheet';
	x_view_type = 'Other receivables';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_or loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

	----- START Farm

	x_root_type = 'Balance Sheet';
	x_view_type = 'Farm';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_farm loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

----- START Greenhouse

	x_root_type = 'Balance Sheet';
	x_view_type = 'Greenhouse';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_greenhouse loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Non operational buildings

	x_root_type = 'Balance Sheet';
	x_view_type = 'Non operational buildings';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_nob loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START Machinery & production equipment

	x_root_type = 'Balance Sheet';
	x_view_type = 'Machinery & production equipment';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_mpe loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Cars & vehicles

	x_root_type = 'Balance Sheet';
	x_view_type = 'Cars & vehicles';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_cv loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START IT & telecom equipment

	x_root_type = 'Balance Sheet';
	x_view_type = 'IT & telecom equipment';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ite loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Office equipment (incl. shop)

	x_root_type = 'Balance Sheet';
	x_view_type = 'Office equipment (incl. shop)';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_oe loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Operational buildings (incl. land)

	x_root_type = 'Balance Sheet';
	x_view_type = 'Operational buildings (incl. land)';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ob loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;




----- START S/T Loans

	x_root_type = 'Balance Sheet';
	x_view_type = 'S/T Loans';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_stl loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Tobacco and raw material

	x_root_type = 'Balance Sheet';
	x_view_type = 'Tobacco and raw material';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_trm loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Semi finished goods

	x_root_type = 'Balance Sheet';
	x_view_type = 'Semi finished goods';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_sfg loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;



----- START Finished and trading goods

	x_root_type = 'Balance Sheet';
	x_view_type = 'Finished and trading goods';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ftg loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Prepaid expenses and accrued income

	x_root_type = 'Balance Sheet';
	x_view_type = 'Prepaid expenses and accrued income';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_peai loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


	----- START Participations

	x_root_type = 'Balance Sheet';
	x_view_type = 'Participations';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_participations loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Deferred taxes

	x_root_type = 'Balance Sheet';
	x_view_type = 'Deferred taxes';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_dt loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START L/T loans

	x_root_type = 'Balance Sheet';
	x_view_type = 'L/T loans';
	x_sub_view_type = 'Balance Sheet';

	for rec in csr_ltl loop
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

            insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;






----- START Material Third


	x_root_type = 'Profit and Loss';
	x_view_type = 'Material third';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_material_third loop
	    if unk='TOT' then
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
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
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
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
			if x_prev_period is null then
				x_prev_period=0;
			end if;
			if x_ori_prev_period is null then
				x_ori_prev_period=0;
			end if;
			raise notice 'x_prev_period: %',x_prev_period;
		end if;

	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Material Group

	x_root_type = 'Profit and Loss';
	x_view_type = 'Material group';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_material_group loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Total material costs & energy

	x_root_type = 'Profit and Loss';
	x_view_type = 'Total material costs & energy';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tot_material loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Personnel expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Personnel expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_personnel_ex loop
		if unk='TOT' then
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
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
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
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
			if x_prev_period is null then
				x_prev_period=0;
			end if;
			if x_ori_prev_period is null then
				x_ori_prev_period=0;
			end if;
			raise notice 'x_prev_period: %',x_prev_period;
		end if;

	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type, unit_kerja)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type, unk);
	end loop;


----- START Sales expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Sales expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_sales_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Transport & logistics

	x_root_type = 'Profit and Loss';
	x_view_type = 'Transport & logistics';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_transport_log loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Advertising expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Advertising expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_advertising_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Facility expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Facility expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_facility_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Maintenance/Repair (excl. facility and vehicles)

	x_root_type = 'Profit and Loss';
	x_view_type = 'Maintenance/Repair (excl. facility and vehicles)';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_maintenance loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Vehicles

	x_root_type = 'Profit and Loss';
	x_view_type = 'Vehicles';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_vehicles loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START IT-Expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Maintenance/Repair (excl. facility and vehicles)';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_it_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Administration expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Administration expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_admin_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Licensing

	x_root_type = 'Profit and Loss';
	x_view_type = 'Licensing';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_licensing loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Total operating expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Total operating expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tot_operating_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Depreciation fixed assets

	x_root_type = 'Profit and Loss';
	x_view_type = 'Depreciation fixed assets';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_depreciation loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Amortization on immat. assets

	x_root_type = 'Profit and Loss';
	x_view_type = 'Amortization on immat. assets';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_amortization loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Gross sales domestic from goods and services

	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales domestic from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_dom loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Gross sales export from goods and services

	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales export from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Gross sales group from goods and services

	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales group from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_group loop
		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Gross sales related comp from goods and services

	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales related comp from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_rel loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Total revenue deductions from goods and services

	x_root_type = 'Profit and Loss';
	x_view_type = 'Total revenue deductions from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tot_rd loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Inventory change finished/semi-finished goods

	x_root_type = 'Profit and Loss';
	x_view_type = 'Inventory change finished/semi-finished goods';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_icf loop
	   if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Other operating Income

	x_root_type = 'Profit and Loss';
	x_view_type = 'Other operating Income';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_ooi loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Interest income

	x_root_type = 'Profit and Loss';
	x_view_type = 'Interest income';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_ii loop
	   if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Dividend income

	x_root_type = 'Profit and Loss';
	x_view_type = 'Dividend income';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_di loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Profit From Participations

	x_root_type = 'Profit and Loss';
	x_view_type = 'Profit From Participations';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_pfp loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Profit On Securities

	x_root_type = 'Profit and Loss';
	x_view_type = 'Profit On Securities';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_pos loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Profit On Currency Exchange

	x_root_type = 'Profit and Loss';
	x_view_type = 'Profit On Currency Exchange';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_poce loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Interest Expenses

	x_root_type = 'Profit and Loss';
	x_view_type = 'Interest Expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_in_ex loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Losses From Participations

	x_root_type = 'Profit and Loss';
	x_view_type = 'Losses From Participations';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_lfp loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Losses On Securities

	x_root_type = 'Profit and Loss';
	x_view_type = 'Losses On Securities';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_los loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Losses On Currency Exchange

	x_root_type = 'Profit and Loss';
	x_view_type = 'Losses On Currency Exchange';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_loce loop
	   if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Non-operating result

	x_root_type = 'Profit and Loss';
	x_view_type = 'Non-operating result';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_non_or loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Extraordinary result

	x_root_type = 'Profit and Loss';
	x_view_type = 'Extraordinary result';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_er loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START IC-postings Group

	x_root_type = 'Profit and Loss';
	x_view_type = 'IC-postings Group';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_icg loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;

----- START Taxes

	x_root_type = 'Profit and Loss';
	x_view_type = 'Taxes';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tax loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;


----- START Minority interests

	x_root_type = 'Profit and Loss';
	x_view_type = 'Minority interests';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_mi loop
	    if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start and t1.date <= date_end and t2.state='posted'
			into x_cur_period, x_ori_cur_period;
		end if;
		raise notice 'x_cur_period: %',x_cur_period;

		if unk='TOT' then
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		else
			select sum (balance), sum (amount_currency)
			from account_move_line t1
			join account_move t2 on t2.id=t1.move_id
			where t1.account_id = rec.x_id and t1.unit_kerja = unk
			and t1.date >= date_start2 and t1.date <= date_end2 and t2.state='posted'
			into x_prev_period, x_ori_prev_period;
		end if;
		raise notice 'x_prev_period: %',x_prev_period;


	        insert into pr_balance_sheet (tgl_mulai, tgl_akhir, account_type, code, name, group_id, cur_period, prev_period, currency,
		    ori_cur_period, ori_prev_period, root_type, view_type, sub_view_type)
			values (date_start, date_end, rec.account_type, rec.x_code, rec.x_name, rec.x_group,
			x_cur_period, x_prev_period, rec.currency,
			x_ori_cur_period, x_ori_prev_period, x_root_type, x_view_type, x_sub_view_type);
	end loop;





END;


$BODY$
LANGUAGE plpgsql;
        """
        )


