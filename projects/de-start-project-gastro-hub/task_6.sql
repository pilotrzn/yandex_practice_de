-- В Gastro Hub решили проверить новую продуктовую гипотезу и поднять цены на капучино. 
-- Маркетологи компании собрали совещание, чтобы обсудить, на сколько стоит поднять цены. 
-- В это время для отчётности использовать старые цены нельзя. 
-- После обсуждения решили увеличить цены на капучино на 20%. 
-- Обновите данные по ценам так, чтобы до завершения обновления никто не воспользовался старыми ценами. 
-- В заведениях, где цены не меняются, данные о меню должны остаться в полном доступе.

BEGIN;

--SELECT r.restaurant_uuid 
--FROM cafe.restaurants r 
--WHERE r.restaurant_menu #>> '{Напиток,Кофе}' IS NOT NULL 
--FOR UPDATE;

WITH drinks AS (
SELECT 
	r.restaurant_uuid,
	r.restaurant_menu #>> '{Напиток,Кофе}'  drink_price
FROM cafe.restaurants r 
WHERE r.restaurant_menu #>> '{Напиток,Кофе}' IS NOT NULL
FOR UPDATE
)
,prices as(
	SELECT 
		restaurant_uuid,
		drink_price,
		(drink_price::integer * ( 1 + (20::numeric / 100)))::integer::text new_price
	FROM drinks
)
UPDATE cafe.restaurants r
SET restaurant_menu = jsonb_set(restaurant_menu::jsonb, '{Напиток,Кофе}', p.new_price::jsonb)
FROM prices p 
WHERE p.restaurant_uuid = r.restaurant_uuid 
RETURNING r.*;

COMMIT;