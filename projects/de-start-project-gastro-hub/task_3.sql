-- Найдите топ-3 заведения, где чаще всего менялся менеджер за весь период.

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