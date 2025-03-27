DELETE
  FROM mart.f_customer_retention
 WHERE period_id =
       (SELECT week_of_year
          FROM mart.d_calendar
         WHERE date_actual::date ='{{ds}}');


WITH all_orders AS (
SELECT dc.week_num,
	   dc.month_num ,
	   uol.item_id,
	uol.customer_id,
	payment_amount,
	uol.status,
	count(uol.payment_amount) OVER (PARTITION BY uol.item_id, uol.customer_id, uol.status) AS cnt
  FROM stage.user_order_log uol
 INNER JOIN mart.d_calendar dc 
    ON uol.date_time::date = dc.fact_date 
   AND dc.week_num = (
              SELECT week_num 
                FROM mart.d_calendar
               WHERE fact_date = '{{ds}}'))
, new_cust_count AS (
	SELECT ao.week_num,
		ao.item_id,
		count(ao.customer_id) new_customer_count,
		sum(ao.payment_amount) new_customers_revenue
	  FROM all_orders  ao
	 WHERE status = 'shipped' AND cnt = 1
	 GROUP BY ao.item_id,ao.week_num
),returning_cust_count AS (
	SELECT ao.week_num,
		ao.item_id,
		count(ao.customer_id) return_customer_count,
		sum(ao.payment_amount) return_customers_revenue
	  FROM all_orders  ao
	 WHERE status = 'shipped' AND cnt > 1
	 GROUP BY ao.item_id,ao.week_num
), refunded_cust_count AS (
	SELECT ao.week_num,
		ao.item_id,
		count(ao.customer_id) refund_customer_count,
		sum(ao.payment_amount) refund_customers_revenue
	  FROM all_orders  ao
	 WHERE status = 'refunded' 
	 GROUP BY ao.item_id,ao.week_num
)
SELECT ncc.new_customer_count,
	rcc.return_customer_count,
	rfcc.refund_customer_count,
	ncc.week_num,
	ncc.item_id,
	ncc.new_customers_revenue,
	rcc.return_customers_revenue,
	rfcc.refund_customers_revenue
  FROM new_cust_count ncc
  LEFT JOIN returning_cust_count rcc 
    ON (ncc.week_num, ncc.item_id) = (rcc.week_num, rcc.item_id)
  LEFT JOIN refunded_cust_count rfcc 
    ON (ncc.week_num, ncc.item_id) = (rfcc.week_num, rfcc.item_id) 
