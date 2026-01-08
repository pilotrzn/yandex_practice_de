-- Найдите пиццерию с самым большим количеством пицц в меню. Если таких пиццерий несколько, выведите все.

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
