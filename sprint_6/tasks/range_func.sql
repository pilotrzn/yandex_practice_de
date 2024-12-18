SELECT *, ROW_NUMBER() OVER()
FROM tools_shop.items i;

WITH users as(
SELECT 
	user_id,
	first_name,
	last_name,
	email,
	created_at, 
ROW_NUMBER () OVER (ORDER BY created_at) rn
FROM tools_shop.users u 
)
SELECT * 
FROM users
WHERE rn = 2021;

WITH ord AS (
SELECT 
	order_id, 
	user_id, 
	total_amt, 
	items_cnt, 
	created_at, 
	paid_at,
	ROW_NUMBER () OVER (PARTITION BY paid_at::date ORDER BY total_amt DESC) rn
FROM tools_shop.orders)
SELECT paid_at::date,
	order_id
FROM ord
WHERE rn = 4;

select *,
rank() over(order by item_id)
from tools_shop.order_x_item;

SELECT *,
dense_rank() over(PARTITION BY u.first_name, u.last_name ORDER BY u.created_at desc)
FROM tools_shop.users u ;

SELECT 
	o.order_id,
	o.user_id,
	o.paid_at,
	lag(paid_at,1,'1980-01-01') over(PARTITION BY user_id ORDER BY o.paid_at) paid_at
FROM tools_shop.orders o ;

SELECT e.event_id ,
e.event_time ,
e.user_id ,
lead(event_time) over(PARTITION BY e.user_id ORDER BY e.event_time)
FROM tools_shop.events e ;

SELECT 
    event_id,
    event_time,
    user_id,
    LEAD(event_time) OVER (PARTITION BY user_id ORDER BY event_time) - event_time AS next_event_time
FROM tools_shop.events;