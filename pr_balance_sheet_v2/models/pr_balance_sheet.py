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
			where (t5.name = 'Cash & Cash equivalents') order by x_code asc;

   

BEGIN

	delete from pr_balance_sheet;
	
	raise notice 'Aktiva - Kas dan Setara Kas';
	
	raise notice 'start loop';


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
	

----- START Material Group
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Material group';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_material_group loop
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


----- START Total material costs & energy
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Total material costs & energy';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tot_material loop
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


----- START Personnel expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Personnel expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_personnel_ex loop
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


----- START Sales expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Sales expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_sales_ex loop
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


----- START Transport & logistics
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Transport & logistics';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_transport_log loop
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


----- START Advertising expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Advertising expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_advertising_ex loop
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


----- START Facility expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Facility expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_facility_ex loop
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


----- START Maintenance/Repair (excl. facility and vehicles)
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Maintenance/Repair (excl. facility and vehicles)';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_maintenance loop
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


----- START Vehicles
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Vehicles';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_vehicles loop
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


----- START IT-Expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Maintenance/Repair (excl. facility and vehicles)';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_it_ex loop
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


----- START Administration expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Administration expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_admin_ex loop
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


----- START Licensing
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Licensing';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_licensing loop
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


----- START Total operating expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Total operating expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tot_operating_ex loop
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


----- START Depreciation fixed assets
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Depreciation fixed assets';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_depreciation loop
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


----- START Amortization on immat. assets
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Amortization on immat. assets';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_amortization loop
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


----- START Gross sales domestic from goods and services
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales domestic from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_dom loop
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


----- START Gross sales export from goods and services
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales export from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_ex loop
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


----- START Gross sales group from goods and services
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales group from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_group loop
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


----- START Gross sales related comp from goods and services
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Gross sales related comp from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_gs_rel loop
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


----- START Total revenue deductions from goods and services
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Total revenue deductions from goods and services';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tot_rd loop
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


----- START Inventory change finished/semi-finished goods
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Inventory change finished/semi-finished goods';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_icf loop
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


----- START Other operating Income
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Other operating Income';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_ooi loop
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


----- START Interest income
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Interest income';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_ii loop
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


----- START Dividend income
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Dividend income';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_di loop
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


----- START Profit From Participations
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Profit From Participations';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_pfp loop
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


----- START Profit On Securities
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Profit On Securities';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_pos loop
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


----- START Profit On Currency Exchange
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Profit On Currency Exchange';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_poce loop
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


----- START Interest Expenses
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Interest Expenses';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_in_ex loop
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


----- START Losses From Participations
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Losses From Participations';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_lfp loop
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


----- START Losses On Securities
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Losses On Securities';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_los loop
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


----- START Losses On Currency Exchange
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Losses On Currency Exchange';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_loce loop
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


----- START Non-operating result
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Non-operating result';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_non_or loop
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


----- START Extraordinary result
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Extraordinary result';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_er loop
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


----- START IC-postings Group
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'IC-postings Group';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_icg loop
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

----- START Taxes
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Taxes';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_tax loop
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


----- START Minority interests
	 
	x_root_type = 'Profit and Loss';
	x_view_type = 'Minority interests';
	x_sub_view_type = 'Profit and Loss';

	for rec in pl_mi loop
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




	
END;


$BODY$
LANGUAGE plpgsql;
        """
        )
    

