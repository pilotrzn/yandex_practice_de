-- Найдите самую дорогую пиццу для каждой пиццерии.

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