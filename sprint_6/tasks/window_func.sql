SELECT 
	o.order_id,
	o.user_id,
	o.total_amt,
	o.items_cnt,
	o.created_at,
	o.paid_at,
	sum(o.total_amt) over(PARTITION BY o.user_id) user_sum,
	sum(o.total_amt) OVER() sum_total
FROM tools_shop.orders o 
ORDER BY o.user_id ;

SELECT u.*, count(*) over()
FROM tools_shop.users u;

SELECT 
	o.order_id,
	o.user_id,
	o.total_amt,
	o.items_cnt,
	o.created_at,
	o.paid_at,
	sum(o.total_amt) over(PARTITION BY o.user_id, date_trunc('month', o.created_at)) user_sum
FROM tools_shop.orders o 
ORDER BY o.user_id ,o.created_at DESC;


SELECT 	o.order_id,
	o.user_id,
	o.total_amt,
	o.items_cnt,
	o.created_at,
	o.paid_at,
	count(*) OVER (PARTITION BY o.created_at::date) orders_cnt
FROM tools_shop.orders o;

SELECT 	
	o.order_id,
	o.user_id,
	o.total_amt,
	o.items_cnt,
	o.created_at,
	o.paid_at,
	round(100 * (o.total_amt / sum(o.total_amt) over(PARTITION BY date_trunc('month', o.paid_at)))) revenue
FROM tools_shop.orders o;

SELECT 	
	o.paid_at,
	o.total_amt,
	sum(o.total_amt) over(order BY  o.paid_at ) cum_sum
FROM tools_shop.orders o;

SELECT 	
	o.user_id,
	o.paid_at,
	o.total_amt,
	sum(o.total_amt) OVER ( PARTITION BY o.user_id ORDER BY o.paid_at ) cum_sum
FROM tools_shop.orders o;

SELECT 	
	date_trunc('month',o.paid_at)::date,
	o.total_amt,
	sum(o.total_amt) OVER ( PARTITION BY date_trunc('month',o.paid_at)::date ORDER BY date_trunc('month',o.paid_at) ) cum_sum
FROM tools_shop.orders o;