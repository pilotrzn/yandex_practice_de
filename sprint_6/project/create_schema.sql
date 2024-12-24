CREATE  SCHEMA cafe;

CREATE TYPE cafe.restaurant_type AS ENUM('coffee_shop', 'restaurant', 'bar', 'pizzeria');

CREATE TABLE cafe.restaurants(
	restaurant_uuid uuid PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
	restaurant_name TEXT,
	restaurant_type cafe.restaurant_type,
	restaurant_menu text
);

CREATE TABLE cafe.managers(
	manager_uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	manager_name TEXT,
	manager_phone text
);

CREATE TABLE cafe.restaurant_manager_work_dates(
	restaurant_uuid uuid NOT NULL,
	manager_uuid uuid NOT NULL,
	begin_work_date date NOT NULL,
	end_work_date date NULL,
	CONSTRAINT rest_man_work_dates_rest_uuid_fkey FOREIGN KEY (restaurant_uuid) REFERENCES  cafe.restaurants(restaurant_uuid),
	CONSTRAINT rest_man_work_dates_manager_uuid_fkey FOREIGN KEY (manager_uuid) REFERENCES  cafe.managers(manager_uuid),
	CONSTRAINT rest_man_work_dates_pkey PRIMARY KEY (restaurant_uuid, manager_uuid)
);

CREATE TABLE cafe.sales(
	sale_date date NOT NULL,
	restaurant_uuid uuid NOT NULL,
	avg_check numeric(6,2),
	CONSTRAINT sales_sale_date_rest_uuid PRIMARY KEY(sale_date, restaurant_uuid)
	);


INSERT INTO cafe.restaurants (restaurant_name, restaurant_type)
SELECT DISTINCT cafe_name ,s."type"::cafe.restaurant_type  
FROM gastrohub.raw_data.sales s 
RETURNING *;

UPDATE cafe.restaurants 
SET restaurant_menu = m.menu 
FROM raw_data.menu m 
where cafe.restaurants.restaurant_name = m.cafe_name 
RETURNING *;

INSERT INTO cafe.managers (manager_name, manager_phone)
SELECT DISTINCT s.manager ,s.manager_phone 
FROM raw_data.sales s 
RETURNING *;

INSERT INTO cafe.restaurant_manager_work_dates(begin_work_date,end_work_date,manager_uuid,restaurant_uuid)
SELECT min(s.report_date), max(s.report_date), m.manager_uuid ,r.restaurant_uuid 
FROM raw_data.sales s 
LEFT JOIN cafe.managers m ON m.manager_name = s.manager 
LEFT JOIN cafe.restaurants r ON r.restaurant_name = s.cafe_name 
GROUP BY m.manager_uuid ,r.restaurant_uuid
RETURNING *;

INSERT INTO cafe.sales(sale_date,restaurant_uuid ,avg_check)
SELECT s.report_date ,r.restaurant_uuid ,s.avg_check 
FROM raw_data.sales s 
LEFT JOIN cafe.restaurants r ON r.restaurant_name = s.cafe_name 
RETURNING *;


CREATE OR REPLACE VIEW cafe.top_restaurants
AS 
WITH avg_checks AS (
    SELECT 
        s.restaurant_uuid,
        avg(s.avg_check) AS avg_check
    FROM cafe.sales s
    GROUP BY s.restaurant_uuid
    )
SELECT 
    restaurant_name AS "Название заведения",
    restaurant_type AS "Тип заведения",
    avg_check AS "Средний чек"
FROM ( 
	    SELECT 
   		    ROW_NUMBER () OVER (PARTITION BY r.restaurant_type ORDER BY ac.avg_check desc) rn,
            r.restaurant_name,
            r.restaurant_type,
            round(ac.avg_check, 2) AS avg_check
        FROM avg_checks ac
        JOIN cafe.restaurants r USING (restaurant_uuid)) t
WHERE rn <= 3;

CREATE MATERIALIZED VIEW cafe.cafe_avg_check_by_year AS 
WITH avgs AS
(
	SELECT 
		EXTRACT(year FROM s.sale_date) AS year,
		s.restaurant_uuid,
		round(avg(s.avg_check), 2) AS avg_check
	FROM cafe.sales s
    WHERE EXTRACT(year FROM s.sale_date) <> 2023::NUMERIC
    GROUP BY s.restaurant_uuid, (EXTRACT(year FROM s.sale_date))
), lags AS (
SELECT 
	r.restaurant_name,
	r.restaurant_type,
	avgs.avg_check,
	lag(avgs.avg_check) OVER (PARTITION BY r.restaurant_name ORDER BY avgs.year) AS last_year_check
FROM cafe.restaurants r
JOIN avgs USING (restaurant_uuid))
SELECT 
	restaurant_name AS "Название заведения",
    restaurant_type AS "Тип заведения",
    avg_check AS "Средний чек в этом году",
    last_year_check AS "Средний чек в предыдущем году",
    round(100::numeric * (avg_check / last_year_check - 1::numeric), 2) AS "Изменение среднего чека в %"
FROM lags;

WITH cnt AS (
SELECT 
	restaurant_uuid,
	count(*) change_count
FROM cafe.restaurant_manager_work_dates rmwd  
GROUP BY restaurant_uuid)
SELECT
	r.restaurant_name "Название заведения",
	cnt.change_count "Сколько раз менялся менеджер"
FROM cnt 
JOIN cafe.restaurants r using(restaurant_uuid)
ORDER BY cnt.change_count DESC 
LIMIT 3;

WITH menus AS (
SELECT 
	r.restaurant_name,
	jsonb_each_text(r.restaurant_menu -> 'Пицца')  pizzas
FROM cafe.restaurants r 
WHERE r.restaurant_type = 'pizzeria'
)
SELECT 
	t.restaurant_name,
	t.cnt
FROM (
SELECT 
	m.restaurant_name,
	count(m.pizzas) cnt,
	DENSE_RANK() OVER (ORDER BY count(m.pizzas) desc) rn
FROM menus m
GROUP BY m.restaurant_name) t
WHERE t.rn = 1;

WITH menu_cte AS (
SELECT 
	r.restaurant_name,
	'Пицца' dish_type,
	(jsonb_each_text(r.restaurant_menu -> 'Пицца')).key  pizza_name,
	(jsonb_each_text(r.restaurant_menu -> 'Пицца')).value::integer  pizza_price
FROM cafe.restaurants r 
WHERE r.restaurant_type = 'pizzeria'
),
menu_with_rank AS (
	SELECT 
	m.restaurant_name,
		m.dish_type,
		ROW_number() OVER (PARTITION BY m.restaurant_name ORDER BY m.pizza_price DESC) rn,
		m.pizza_name,
		m.pizza_price
	FROM menu_cte m
)
SELECT  
	restaurant_name,
	dish_type,
	pizza_name,
	pizza_price
FROM menu_with_rank WHERE rn = 1;