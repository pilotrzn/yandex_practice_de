CREATE TABLE public.outbox(
	id int GENERATED ALWAYS AS IDENTITY,
	object_id int NOT NULL,
	record_ts timestamp NOT NULL,
	TYPE varchar NOT NULL,
	payload TEXT,
	CONSTRAINT outbox_id_pk PRIMARY key(id)
);

DROP MATERIALIZED VIEW IF EXISTS dwh.orders_report_materialized_view;

CREATE MATERIALIZED VIEW IF NOT EXISTS dwh.orders_report_materialized_view
AS
SELECT 
	sum(T1.product_price) total_money,
	count(T1.product_name) total_products,
	avg(T1.craftsman_age) avg_age_craftsman,
	avg(T1.customer_age)  avg_age_customer,			
	sum(CASE WHEN T1.order_status = 'created' THEN 1 ELSE 0 END) count_order_created,
	sum(CASE WHEN T1.order_status = 'in progress' THEN 1 ELSE 0 END) count_order_in_progress,
	sum(CASE WHEN T1.order_status = 'delivery' THEN 1 ELSE 0 END) count_order_delivery,
	sum(CASE WHEN T1.order_status = 'done' THEN 1 ELSE 0 END) count_order_done,
	sum(CASE WHEN T1.order_status != 'done' THEN 1 ELSE 0 END) count_order_not_done,
	avg(T2.diff_order_date) avg_days_complete_orders,
	percentile_cont(0.5) WITHIN GROUP(ORDER BY T2.diff_order_date) median_days_complete_orders,
	T1.report_period
FROM
	(SELECT 	
		fo.order_id AS order_id, 
		fo.order_completion_date AS order_completion_date,
		fo.order_created_date AS order_created_date,
		dp.product_price AS product_price,
		dp.product_name AS product_name,
		fo.order_status AS order_status, 
		to_char(fo.order_created_date, 'yyyy-mm') AS report_period, 
		extract(YEAR FROM current_timestamp) - date_part('year', dc.craftsman_birthday) AS craftsman_age, 
		extract(YEAR FROM current_timestamp) - date_part('year', dcs.customer_birthday) AS customer_age 
	FROM dwh.f_order fo 
	INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id  = dc.craftsman_id 
	INNER JOIN dwh.d_customer dcs ON fo.customer_id  = dcs.customer_id  
	INNER JOIN dwh.d_product dp ON dp.product_id  = fo.product_id) AS T1
	LEFT JOIN (
			SELECT 	
			  	inner_fo.order_id,
			  	inner_fo.order_completion_date - inner_fo.order_created_date AS diff_order_date 
		 	FROM dwh.f_order inner_fo
			WHERE inner_fo.order_status = 'done' 
		  	AND inner_fo.order_completion_date IS NOT NULL) T2 
		  	ON T1.order_id = T2.order_id
	GROUP BY T1.report_period
	ORDER BY total_money;
