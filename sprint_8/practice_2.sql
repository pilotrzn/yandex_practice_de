
--1
DROP TABLE IF EXISTS dwh.load_dates_craftsman_report_datamart;

CREATE TABLE IF NOT EXISTS dwh.load_dates_craftsman_report_datamart (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    load_dttm date NOT NULL,
    constraint load_dates_craftsman_report_datamart_pk primary key(id)
);

--2
DROP TABLE IF EXISTS dwh.dwh_delta;
CREATE TABLE IF NOT EXISTS dwh.dwh_delta AS (
SELECT 
	dc.craftsman_id,
	dc.craftsman_name,
	dc.craftsman_address,
	dc.craftsman_birthday,
	dc.craftsman_email,
	fo.order_id,
	dp.product_id,
	dp.product_price,
	dp.product_type,
	extract(YEAR FROM current_timestamp) - date_part('year', dcs.customer_birthday) customer_age,
    fo.order_completion_date - fo.order_created_date diff_order_date,
    fo.order_status,
    to_char(fo.order_created_date, 'yyyy-mm') report_period,
	crd.id exist_craftsman_id,
	dc.load_dttm  craftsman_load_dttm,
	dcs.load_dttm customers_load_dttm,
	dp.load_dttm products_load_dttm
FROM dwh.f_order fo 
INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id  = dc.craftsman_id 
INNER JOIN dwh.d_customer dcs ON fo.customer_id  = dcs.customer_id  
INNER JOIN dwh.d_product dp ON dp.product_id  = fo.product_id 
LEFT JOIN dwh.load_dates_craftsman_report_datamart crd ON crd.id = dc.craftsman_id 
WHERE fo.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_craftsman_report_datamart)) OR
                            (dc.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_craftsman_report_datamart)) OR
                            (dcs.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_craftsman_report_datamart)) OR
                            (dp.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_craftsman_report_datamart))
);

--3
DROP TABLE IF EXISTS dwh.dwh_update_delta;
CREATE TABLE IF NOT EXISTS dwh.dwh_update_delta AS 
SELECT dd.craftsman_id
FROM dwh.dwh_delta dd
WHERE dd.exist_craftsman_id IS NOT null;


--4
DROP TABLE IF EXISTS dwh.dwh_delta_insert_result;
CREATE TABLE IF NOT EXISTS dwh.dwh_delta_insert_result AS (
	SELECT  
		T4.craftsman_id AS craftsman_id,
		T4.craftsman_name AS craftsman_name,
		T4.craftsman_address AS craftsman_address,
		T4.craftsman_birthday AS craftsman_birthday,
		T4.craftsman_email AS craftsman_email,
		T4.craftsman_money AS craftsman_money,
		T4.platform_money AS platform_money,
		T4.count_order AS count_order,
		T4.avg_price_order AS avg_price_order,
		T4.avg_age_customer AS avg_age_customer,
		T4.product_type AS top_product_category,
		T4.median_time_order_completed AS median_time_order_completed,
		T4.count_order_created AS count_order_created,
		T4.count_order_in_progress AS count_order_in_progress,
		T4.count_order_delivery AS count_order_delivery,
		T4.count_order_done AS count_order_done,
		T4.count_order_not_done AS count_order_not_done,
		T4.report_period AS report_period 
	FROM (
		 	SELECT 	*,
				RANK() OVER(PARTITION BY T2.craftsman_id ORDER BY count_product DESC) AS rank_count_product 
			FROM ( 
                SELECT 
						T1.craftsman_id ,
						T1.craftsman_name ,
						T1.craftsman_address ,
						T1.craftsman_birthday ,
						T1.craftsman_email ,
						sum(T1.product_price) * 0.9 craftsman_money,
						sum(T1.product_price) * 0.1 platform_money,
						count(T1.order_id) count_order,
						avg(T1.product_price) avg_price_order,
						avg(T1.customer_age) avg_age_customer,
						percentile_cont(0.5) WITHIN GROUP(ORDER BY T1.diff_order_date) median_time_order_completed,
						sum(CASE WHEN order_status = 'created' THEN 1 ELSE 0 END) count_order_created,
						sum(CASE WHEN order_status = 'in progress' THEN 1 ELSE 0 END) count_order_in_progress,
						sum(CASE WHEN order_status = 'delivery' THEN 1 ELSE 0 END) count_order_delivery,
						sum(CASE WHEN order_status = 'done' THEN 1 ELSE 0 END) count_order_done,
						sum(CASE WHEN order_status != 'done' THEN 1 ELSE 0 END) count_order_not_done,
						T1.report_period 
					FROM dwh.dwh_delta AS T1
					WHERE T1.exist_craftsman_id IS NULL
					GROUP BY 
						T1.craftsman_id, 
						T1.craftsman_name, 
						T1.craftsman_address, 
						T1.craftsman_birthday, 
						T1.craftsman_email, 
						T1.report_period
				) AS T2 
			INNER JOIN (
						SELECT 
							dd.craftsman_id craftsman_id_for_product_type,
							dd.product_type,
							count(product_id) count_product,
							ROW_NUMBER() OVER (PARTITION BY dd.craftsman_id ORDER BY dd.product_type) rank_count
						FROM dwh.dwh_delta dd 
						GROUP BY dd.craftsman_id, dd.product_type
						ORDER BY count_product DESC) AS T3 
			ON T2.craftsman_id = T3.craftsman_id_for_product_type
	) AS T4 
	WHERE T4.rank_count_product = 1 
	ORDER BY report_period
	);

--5
DROP TABLE IF EXISTS dwh.dwh_delta_update_result;
CREATE TABLE IF NOT EXISTS dwh.dwh_delta_update_result AS ( 
SELECT 
	T4.craftsman_id AS craftsman_id,
	T4.craftsman_name AS craftsman_name,
	T4.craftsman_address AS craftsman_address,
	T4.craftsman_birthday AS craftsman_birthday,
	T4.craftsman_email AS craftsman_email,
	T4.craftsman_money AS craftsman_money,
	T4.platform_money AS platform_money,
	T4.count_order AS count_order,
	T4.avg_price_order AS avg_price_order,
	T4.avg_age_customer AS avg_age_customer,
	T4.product_type AS top_product_category,
	T4.median_time_order_completed AS median_time_order_completed,
	T4.count_order_created AS count_order_created,
	T4.count_order_in_progress AS count_order_in_progress,
	T4.count_order_delivery AS count_order_delivery, 
	T4.count_order_done AS count_order_done, 
	T4.count_order_not_done AS count_order_not_done,
	T4.report_period AS report_period 
FROM (
	SELECT 	*,
		RANK() OVER(PARTITION BY T2.craftsman_id ORDER BY count_product DESC) AS rank_count_product 
	FROM (
			SELECT 
				T1.craftsman_id AS craftsman_id,
				T1.craftsman_name AS craftsman_name,
				T1.craftsman_address AS craftsman_address,
				T1.craftsman_birthday AS craftsman_birthday,
				T1.craftsman_email AS craftsman_email,
				SUM(T1.product_price) - (SUM(T1.product_price) * 0.1) AS craftsman_money,
				SUM(T1.product_price) * 0.1 AS platform_money,
				COUNT(order_id) AS count_order,
				AVG(T1.product_price) AS avg_price_order,
				AVG(T1.customer_age) AS avg_age_customer,
				PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY diff_order_date) AS median_time_order_completed,
				SUM(CASE WHEN T1.order_status = 'created' THEN 1 ELSE 0 END) AS count_order_created, 
				SUM(CASE WHEN T1.order_status = 'in progress' THEN 1 ELSE 0 END) AS count_order_in_progress, 
				SUM(CASE WHEN T1.order_status = 'delivery' THEN 1 ELSE 0 END) AS count_order_delivery, 
				SUM(CASE WHEN T1.order_status = 'done' THEN 1 ELSE 0 END) AS count_order_done, 
				SUM(CASE WHEN T1.order_status != 'done' THEN 1 ELSE 0 END) AS count_order_not_done,
				T1.report_period AS report_period
				FROM (
					SELECT 	
						dc.craftsman_id AS craftsman_id,
						dc.craftsman_name AS craftsman_name,
						dc.craftsman_address AS craftsman_address,
						dc.craftsman_birthday AS craftsman_birthday,
						dc.craftsman_email AS craftsman_email,
						fo.order_id AS order_id,
						dp.product_id AS product_id,
						dp.product_price AS product_price,
						dp.product_type AS product_type,
						extract(YEAR FROM current_timestamp) - date_part('year', dcs.customer_birthday) customer_age,
						fo.order_completion_date - fo.order_created_date diff_order_date,
						fo.order_status AS order_status,
						to_char(fo.order_created_date, 'yyyy-mm') report_period
					FROM dwh.f_order fo 
					INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id = dc.craftsman_id 
					INNER JOIN dwh.d_customer dcs ON fo.customer_id = dcs.customer_id 
					INNER JOIN dwh.d_product dp ON fo.product_id = dp.product_id
					INNER JOIN dwh.dwh_update_delta ud ON fo.craftsman_id = ud.craftsman_id
				) AS T1
				GROUP BY 
					T1.craftsman_id,
					T1.craftsman_name,
					T1.craftsman_address,
					T1.craftsman_birthday,
					T1.craftsman_email,
					T1.report_period
					) AS T2 
				INNER JOIN (
							SELECT 
								dd.craftsman_id craftsman_id_for_product_type,
								dd.product_type,
								count(product_id) count_product,
								ROW_NUMBER() OVER (PARTITION BY dd.craftsman_id ORDER BY dd.product_type) rank_count
							FROM dwh_delta dd 
							GROUP BY dd.craftsman_id, dd.product_type
							ORDER BY count_product DESC) AS T3 
				ON T2.craftsman_id = T3.craftsman_id_for_product_type
	) AS T4 
	WHERE T4.rank_count_product = 1 
	ORDER BY report_period
);

--6
INSERT INTO dwh.craftsman_report_datamart
	(craftsman_id, 
	craftsman_name, 
	craftsman_address, 
	craftsman_birthday, 
	craftsman_email, 
	craftsman_money, 
	platform_money, 
	count_order, 
	avg_price_order, 
	avg_age_customer, 
	median_time_order_completed, 
	top_product_category, 
	count_order_created, 
	count_order_in_progress, 
	count_order_delivery, 
	count_order_done, 
	count_order_not_done, 
	report_period)
SELECT 
	craftsman_id, 
	craftsman_name, 
	craftsman_address, 
	craftsman_birthday, 
	craftsman_email, 
	craftsman_money, 
	platform_money, 
	count_order, 
	avg_price_order, 
	avg_age_customer,  
	median_time_order_completed, 
	top_product_category,
	count_order_created, 
	count_order_in_progress, 
	count_order_delivery, 
	count_order_done, 
	count_order_not_done, 
	report_period
FROM dwh.dwh_delta_insert_result;

--7
UPDATE dwh.craftsman_report_datamart
SET craftsman_name = updates.craftsman_name,
	craftsman_address = updates.craftsman_address, 
	craftsman_birthday = updates.craftsman_birthday,
	craftsman_email = updates.craftsman_email,
	craftsman_money = updates.craftsman_money, 
	platform_money = updates.platform_money, 
	count_order = updates.count_order, 
	avg_price_order = updates.avg_price_order, 
	avg_age_customer = updates.avg_age_customer, 
	median_time_order_completed = updates.median_time_order_completed, 
	top_product_category = updates.top_product_category, 
	count_order_created = updates.count_order_created, 
	count_order_in_progress = updates.count_order_in_progress, 
	count_order_delivery = updates.count_order_delivery, 
	count_order_done = updates.count_order_done, 
	count_order_not_done = updates.count_order_not_done, 
	report_period = updates.report_period
FROM (
	SELECT 
		craftsman_id,
		craftsman_name, 
		craftsman_address, 
		craftsman_birthday, 
		craftsman_email, 
		craftsman_money, 
		platform_money, 
		count_order, 
		avg_price_order, 
		avg_age_customer, 
		top_product_category, 
		median_time_order_completed, 
		count_order_created, 
		count_order_in_progress, 
		count_order_delivery, 
		count_order_done, 
		count_order_not_done, 
		report_period
	FROM dwh.dwh_delta_update_result) AS updates
WHERE updates.craftsman_id = dwh.craftsman_report_datamart.craftsman_id ;

--8
INSERT INTO dwh.load_dates_craftsman_report_datamart 
(load_dttm)
SELECT 
coalesce(
	GREATEST(
		max(dd.craftsman_load_dttm),
		max(dd.customers_load_dttm),
		max(dd.products_load_dttm)),now())
FROM dwh.dwh_delta dd;


------------------
WITH
dwh_delta AS (
	SELECT 
		dc.craftsman_id,
		dc.craftsman_name,
		dc.craftsman_address,
		dc.craftsman_birthday,
		dc.craftsman_email,
		fo.order_id,
		dp.product_id,
		dp.product_price,
		dp.product_type,
		extract(YEAR FROM current_timestamp) - date_part('year', dcs.customer_birthday) customer_age,
	    fo.order_completion_date - fo.order_created_date diff_order_date,
	    fo.order_status,
	    to_char(fo.order_created_date, 'yyyy-mm') report_period,
		crd.id exist_craftsman_id,
		dc.load_dttm  craftsman_load_dttm,
		dcs.load_dttm customers_load_dttm,
		dp.load_dttm products_load_dttm
	FROM dwh.f_order fo 
	INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id  = dc.craftsman_id 
	INNER JOIN dwh.d_customer dcs ON fo.customer_id  = dcs.customer_id  
	INNER JOIN dwh.d_product dp ON dp.product_id  = fo.product_id 
	LEFT JOIN dwh.load_dates_craftsman_report_datamart crd ON crd.id = dc.craftsman_id 
	WHERE fo.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_craftsman_report_datamart)
),
dwh_update_delta AS (
	SELECT dd.craftsman_id
	FROM dwh_delta dd
	WHERE dd.exist_craftsman_id IS NOT null
),
dwh_delta_insert_result AS (
	SELECT  
		T4.craftsman_id AS craftsman_id,
		T4.craftsman_name AS craftsman_name,
		T4.craftsman_address AS craftsman_address,
		T4.craftsman_birthday AS craftsman_birthday,
		T4.craftsman_email AS craftsman_email,
		T4.craftsman_money AS craftsman_money,
		T4.platform_money AS platform_money,
		T4.count_order AS count_order,
		T4.avg_price_order AS avg_price_order,
		T4.avg_age_customer AS avg_age_customer,
		T4.product_type AS top_product_category,
		T4.median_time_order_completed AS median_time_order_completed,
		T4.count_order_created AS count_order_created,
		T4.count_order_in_progress AS count_order_in_progress,
		T4.count_order_delivery AS count_order_delivery,
		T4.count_order_done AS count_order_done,
		T4.count_order_not_done AS count_order_not_done,
		T4.report_period AS report_period 
	FROM (
		 	SELECT 	*,
				RANK() OVER(PARTITION BY T2.craftsman_id ORDER BY count_product DESC) AS rank_count_product 
			FROM ( 
                SELECT 
						T1.craftsman_id ,
						T1.craftsman_name ,
						T1.craftsman_address ,
						T1.craftsman_birthday ,
						T1.craftsman_email ,
						sum(T1.product_price) * 0.9 craftsman_money,
						sum(T1.product_price) * 0.1 platform_money,
						count(T1.order_id) count_order,
						avg(T1.product_price) avg_price_order,
						avg(T1.customer_age) avg_age_customer,
						percentile_cont(0.5) WITHIN GROUP(ORDER BY T1.diff_order_date) median_time_order_completed,
						sum(CASE WHEN order_status = 'created' THEN 1 ELSE 0 END) count_order_created,
						sum(CASE WHEN order_status = 'in progress' THEN 1 ELSE 0 END) count_order_in_progress,
						sum(CASE WHEN order_status = 'delivery' THEN 1 ELSE 0 END) count_order_delivery,
						sum(CASE WHEN order_status = 'done' THEN 1 ELSE 0 END) count_order_done,
						sum(CASE WHEN order_status != 'done' THEN 1 ELSE 0 END) count_order_not_done,
						T1.report_period 
					FROM dwh_delta AS T1
					WHERE T1.exist_craftsman_id IS NULL
					GROUP BY 
						T1.craftsman_id, 
						T1.craftsman_name, 
						T1.craftsman_address, 
						T1.craftsman_birthday, 
						T1.craftsman_email, 
						T1.report_period
				) AS T2 
			INNER JOIN (
						SELECT 
							dd.craftsman_id craftsman_id_for_product_type,
							dd.product_type,
							count(product_id) count_product,
							ROW_NUMBER() OVER (PARTITION BY dd.craftsman_id ORDER BY dd.product_type) rank_count
						FROM dwh_delta dd 
						GROUP BY dd.craftsman_id, dd.product_type
						ORDER BY count_product DESC) AS T3 
			ON T2.craftsman_id = T3.craftsman_id_for_product_type
	) AS T4 
	WHERE T4.rank_count_product = 1 
	ORDER BY report_period
),
dwh_delta_update_result AS (
SELECT 
	T4.craftsman_id AS craftsman_id,
	T4.craftsman_name AS craftsman_name,
	T4.craftsman_address AS craftsman_address,
	T4.craftsman_birthday AS craftsman_birthday,
	T4.craftsman_email AS craftsman_email,
	T4.craftsman_money AS craftsman_money,
	T4.platform_money AS platform_money,
	T4.count_order AS count_order,
	T4.avg_price_order AS avg_price_order,
	T4.avg_age_customer AS avg_age_customer,
	T4.product_type AS top_product_category,
	T4.median_time_order_completed AS median_time_order_completed,
	T4.count_order_created AS count_order_created,
	T4.count_order_in_progress AS count_order_in_progress,
	T4.count_order_delivery AS count_order_delivery, 
	T4.count_order_done AS count_order_done, 
	T4.count_order_not_done AS count_order_not_done,
	T4.report_period AS report_period 
FROM (
	SELECT 	*,
		RANK() OVER(PARTITION BY T2.craftsman_id ORDER BY count_product DESC) AS rank_count_product 
	FROM (
			SELECT 
				T1.craftsman_id AS craftsman_id,
				T1.craftsman_name AS craftsman_name,
				T1.craftsman_address AS craftsman_address,
				T1.craftsman_birthday AS craftsman_birthday,
				T1.craftsman_email AS craftsman_email,
				SUM(T1.product_price) - (SUM(T1.product_price) * 0.1) AS craftsman_money,
				SUM(T1.product_price) * 0.1 AS platform_money,
				COUNT(order_id) AS count_order,
				AVG(T1.product_price) AS avg_price_order,
				AVG(T1.customer_age) AS avg_age_customer,
				PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY diff_order_date) AS median_time_order_completed,
				SUM(CASE WHEN T1.order_status = 'created' THEN 1 ELSE 0 END) AS count_order_created, 
				SUM(CASE WHEN T1.order_status = 'in progress' THEN 1 ELSE 0 END) AS count_order_in_progress, 
				SUM(CASE WHEN T1.order_status = 'delivery' THEN 1 ELSE 0 END) AS count_order_delivery, 
				SUM(CASE WHEN T1.order_status = 'done' THEN 1 ELSE 0 END) AS count_order_done, 
				SUM(CASE WHEN T1.order_status != 'done' THEN 1 ELSE 0 END) AS count_order_not_done,
				T1.report_period AS report_period
				FROM (
					SELECT 	
						dc.craftsman_id AS craftsman_id,
						dc.craftsman_name AS craftsman_name,
						dc.craftsman_address AS craftsman_address,
						dc.craftsman_birthday AS craftsman_birthday,
						dc.craftsman_email AS craftsman_email,
						fo.order_id AS order_id,
						dp.product_id AS product_id,
						dp.product_price AS product_price,
						dp.product_type AS product_type,
						extract(YEAR FROM current_timestamp) - date_part('year', dcs.customer_birthday) customer_age,
						fo.order_completion_date - fo.order_created_date diff_order_date,
						fo.order_status AS order_status,
						to_char(fo.order_created_date, 'yyyy-mm') report_period
					FROM dwh.f_order fo 
					INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id = dc.craftsman_id 
					INNER JOIN dwh.d_customer dcs ON fo.customer_id = dcs.customer_id 
					INNER JOIN dwh.d_product dp ON fo.product_id = dp.product_id
					INNER JOIN dwh_update_delta ud ON fo.craftsman_id = ud.craftsman_id
				) AS T1
				GROUP BY 
					T1.craftsman_id,
					T1.craftsman_name,
					T1.craftsman_address,
					T1.craftsman_birthday,
					T1.craftsman_email,
					T1.report_period
					) AS T2 
				INNER JOIN (
							SELECT 
								dd.craftsman_id craftsman_id_for_product_type,
								dd.product_type,
								count(product_id) count_product,
								ROW_NUMBER() OVER (PARTITION BY dd.craftsman_id ORDER BY dd.product_type) rank_count
							FROM dwh_delta dd 
							GROUP BY dd.craftsman_id, dd.product_type
							ORDER BY count_product DESC) AS T3 
				ON T2.craftsman_id = T3.craftsman_id_for_product_type
	) AS T4 
	WHERE T4.rank_count_product = 1 
	ORDER BY report_period
),
insert_delta AS (
INSERT INTO dwh.craftsman_report_datamart
	(craftsman_id, 
	craftsman_name, 
	craftsman_address, 
	craftsman_birthday, 
	craftsman_email, 
	craftsman_money, 
	platform_money, 
	count_order, 
	avg_price_order, 
	avg_age_customer, 
	median_time_order_completed, 
	top_product_category, 
	count_order_created, 
	count_order_in_progress, 
	count_order_delivery, 
	count_order_done, 
	count_order_not_done, 
	report_period)
SELECT 
	craftsman_id, 
	craftsman_name, 
	craftsman_address, 
	craftsman_birthday, 
	craftsman_email, 
	craftsman_money, 
	platform_money, 
	count_order, 
	avg_price_order, 
	avg_age_customer,  
	median_time_order_completed, 
	top_product_category,
	count_order_created, 
	count_order_in_progress, 
	count_order_delivery, 
	count_order_done, 
	count_order_not_done, 
	report_period
FROM dwh_delta_insert_result
),
update_delta AS (
UPDATE dwh.craftsman_report_datamart
SET craftsman_name = updates.craftsman_name,
	craftsman_address = updates.craftsman_address, 
	craftsman_birthday = updates.craftsman_birthday,
	craftsman_email = updates.craftsman_email,
	craftsman_money = updates.craftsman_money, 
	platform_money = updates.platform_money, 
	count_order = updates.count_order, 
	avg_price_order = updates.avg_price_order, 
	avg_age_customer = updates.avg_age_customer, 
	median_time_order_completed = updates.median_time_order_completed, 
	top_product_category = updates.top_product_category, 
	count_order_created = updates.count_order_created, 
	count_order_in_progress = updates.count_order_in_progress, 
	count_order_delivery = updates.count_order_delivery, 
	count_order_done = updates.count_order_done, 
	count_order_not_done = updates.count_order_not_done, 
	report_period = updates.report_period
FROM (
	SELECT 
		craftsman_id,
		craftsman_name, 
		craftsman_address, 
		craftsman_birthday, 
		craftsman_email, 
		craftsman_money, 
		platform_money, 
		count_order, 
		avg_price_order, 
		avg_age_customer, 
		top_product_category, 
		median_time_order_completed, 
		count_order_created, 
		count_order_in_progress, 
		count_order_delivery, 
		count_order_done, 
		count_order_not_done, 
		report_period
	FROM dwh_delta_update_result) AS updates
	WHERE updates.craftsman_id = dwh.craftsman_report_datamart.craftsman_id 
),
insert_load_date AS (
INSERT INTO dwh.load_dates_craftsman_report_datamart 
(load_dttm)
SELECT 
coalesce(
	GREATEST(
		max(dd.craftsman_load_dttm),
		max(dd.customers_load_dttm),
		max(dd.products_load_dttm)),now())
FROM dwh_delta dd
)
SELECT 'increment datamart';