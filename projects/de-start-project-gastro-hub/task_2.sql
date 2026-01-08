-- Создайте материализованное представление, которое покажет, 
-- как изменяется средний чек для каждого заведения от года к году за все года за исключением 2023 года. 
-- Все столбцы со средним чеком округлите до второго знака после запятой.

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
JOIN avgs USING (restaurant_uuid)
)
SELECT 
	restaurant_name AS "Название заведения",
	restaurant_type AS "Тип заведения",
	avg_check AS "Средний чек в этом году",
	last_year_check AS "Средний чек в предыдущем году",
	round(100::numeric * (avg_check / last_year_check - 1::numeric), 2) AS "Изменение среднего чека в %"
FROM lags;