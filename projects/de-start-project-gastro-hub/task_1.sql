-- Чтобы выдать премию менеджерам, нужно понять, у каких заведений самый высокий средний чек. 
-- Создайте представление, которое покажет топ-3 заведения внутри каждого типа заведений по среднему чеку за все даты. 
-- Столбец со средним чеком округлите до второго знака после запятой.


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