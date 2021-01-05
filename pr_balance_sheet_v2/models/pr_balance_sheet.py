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

	csr_aktiva_tidak_lancar CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Non-current Assets');

	csr_aktiva_tetap CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Fixed Assets');
	
	csr_hutang_lancar CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Payable' or t5.name = 'Current Liabilities');

	csr_hutang_jangka_panjang CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Non-current Liabilities');

	csr_modal CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Equity' or t5.name = 'Current Year Earnings');

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
			where (t5.name = 'Cost of Revenue');

	csr_beban_adm CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Expenses' or t5.name = 'Depreciation');

	csr_pendapatan_lain CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Income');

	csr_beban_lain CURSOR FOR 
		select t1.id as x_id, t1.code as x_code, t1.name x_name, 
			t4.name as currency,
			t5.name as account_type
			from account_account t1
			left join res_currency t4 on t1.currency_id = t4.id
			join account_account_type t5 on t1.user_type_id = t5.id	
			where (t5.name = 'Other Expenses');
   

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
	


	
END;


$BODY$
LANGUAGE plpgsql;
        """
        )
    

