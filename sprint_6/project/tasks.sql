
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

WITH drinks AS (
SELECT 
	r.restaurant_uuid,
	(jsonb_each_text(r.restaurant_menu -> 'Напиток')).key drink_name,
	(jsonb_each_text(r.restaurant_menu -> 'Напиток')).value  drink_price
FROM cafe.restaurants r)
,prices as(
	SELECT 
		restaurant_uuid,
		drink_name,
		(drink_price::integer * ( 1 + (20::numeric /100)))::integer::text new_price
	FROM drinks
	WHERE drink_name = 'Кофе'
)
UPDATE cafe.restaurants r
SET restaurant_menu = jsonb_set(restaurant_menu::jsonb, '{Напиток,Кофе}', p.new_price::TEXT::jsonb)
FROM prices p 
WHERE p.restaurant_uuid = r.restaurant_uuid 
RETURNING *;