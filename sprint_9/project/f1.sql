WITH dwh_delta as(
SELECT	dcs.customer_id,
		dcs.customer_name ,
		dcs.customer_address ,
		dcs.customer_birthday ,
		dcs.customer_email ,
	fo.order_id,
	dp.product_id,
	dp.product_price,
	dp.product_type,
    fo.order_completion_date - fo.order_created_date diff_order_date,
    fo.order_status,
    to_char(fo.order_created_date, 'yyyy-mm') report_period,
	crd.id exist_customer_id,
	dcs.load_dttm craftsman_load_dttm,
	dcs.load_dttm customers_load_dttm,
	dp.load_dttm products_load_dttm
FROM dwh.f_order fo 
INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id  = dc.craftsman_id 
INNER JOIN dwh.d_customer dcs ON fo.customer_id  = dcs.customer_id  
INNER JOIN dwh.d_product dp ON dp.product_id  = fo.product_id 
LEFT JOIN dwh.load_dates_customer_report_datamart crd ON crd.id = dcs.customer_id 
WHERE (fo.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_customer_report_datamart)) 
OR    (dc.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_customer_report_datamart)) 
OR    (dcs.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_customer_report_datamart)) 
OR    (dp.load_dttm > (SELECT COALESCE(MAX(load_dttm),'1900-01-01') FROM dwh.load_dates_customer_report_datamart))
),
dwh_update_delta as(
	SELECT dd.customer_id
	FROM   dwh_delta dd
	WHERE  dd.exist_customer_id IS NOT NULL
),