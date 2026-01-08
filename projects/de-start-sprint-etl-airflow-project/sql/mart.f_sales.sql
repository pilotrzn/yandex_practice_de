DELETE FROM mart.f_daily_sales
WHERE date_id = (
        select date_id from mart.d_calendar where fact_date::Date = '{{ds}}'
        );

insert into mart.f_daily_sales(date_id, item_id, customer_id, price, quantity, payment_amount)
SELECT dc.date_id ,u.item_id ,u.customer_id, 
avg(u.payment_amount / u.quantity)  AS price, sum(u.quantity) AS quantity, 
sum(u.payment_amount * (CASE WHEN u.status = 'refunded' THEN -1 ELSE 1 END)) AS payment_amount
FROM stage.user_order_log u
INNER JOIN mart.d_calendar dc ON dc.fact_date = u.date_time and u.date_time::Date = '{{ds}}'
GROUP BY dc.date_id ,u.item_id ,u.customer_id;