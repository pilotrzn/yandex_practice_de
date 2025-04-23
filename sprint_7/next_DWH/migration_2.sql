/* собираем временную таблицу с данными из всех источников */
DROP TABLE IF EXISTS tmp_sources;
CREATE TEMP TABLE tmp_sources AS 
SELECT  order_id,
		order_created_date,
		order_completion_date,
		order_status,
		craftsman_id,
		craftsman_name,
		craftsman_address,
		craftsman_birthday,
		craftsman_email,
		product_id,
		product_name,
		product_description,
		product_type,
		product_price,
		customer_id,
		customer_name,
		customer_address,
		customer_birthday,
		customer_email 
  FROM source1.craft_market_wide
UNION
SELECT  t2.order_id,
		t2.order_created_date,
		t2.order_completion_date,
		t2.order_status,
		t1.craftsman_id,
		t1.craftsman_name,
		t1.craftsman_address,
		t1.craftsman_birthday,
		t1.craftsman_email,
		t1.product_id,
		t1.product_name,
		t1.product_description,
		t1.product_type,
		t1.product_price,
		t2.customer_id,
		t2.customer_name,
		t2.customer_address,
		t2.customer_birthday,
		t2.customer_email 
  FROM source2.craft_market_masters_products t1 
    JOIN source2.craft_market_orders_customers t2 ON t2.product_id = t1.product_id and t1.craftsman_id = t2.craftsman_id 
UNION
SELECT  t1.order_id,
		t1.order_created_date,
		t1.order_completion_date,
		t1.order_status,
		t2.craftsman_id,
		t2.craftsman_name,
		t2.craftsman_address,
		t2.craftsman_birthday,
		t2.craftsman_email,
		t1.product_id,
		t1.product_name,
		t1.product_description,
		t1.product_type,
		t1.product_price,
		t3.customer_id,
		t3.customer_name,
		t3.customer_address,
		t3.customer_birthday,
		t3.customer_email
  FROM source3.craft_market_orders t1
    JOIN source3.craft_market_craftsmans t2 ON t1.craftsman_id = t2.craftsman_id 
    JOIN source3.craft_market_customers t3 ON t1.customer_id = t3.customer_id;

/* заполнение таблицы фактов "Заказы" */
INSERT INTO dwh.f_order(
	product_id, -- идентификатор товара
	craftsman_id, -- идентификатор мастера
	customer_id, -- идентификатор заказчика
	order_created_date, -- дата создания заказа
	order_completion_date, -- дата выполнения заказа
	order_status, -- статус выполнения заказа (created, in progress, delivery, done)
	load_dttm -- дата и время загрузки
	)
SELECT 	dp.product_id ,
		dc.craftsman_id ,
  		dcust.customer_id ,
 		src.order_created_date,
 		src.order_completion_date,
 		src.order_status,
	     dp.load_dttm -- дата и время загрузки
   FROM tmp_sources src
   join dwh.d_craftsman dc ON dc.craftsman_name = src.craftsman_name and dc.craftsman_email = src.craftsman_email 
   join dwh.d_customer dcust ON dcust.customer_name = src.customer_name and dcust.customer_email = src.customer_email 
   join dwh.d_product dp ON dp.product_name = src.product_name and dp.product_description = src.product_description and dp.product_price = src.product_price;
