WITH top_movies as(
SELECT 
	title,
	rental_rate,
	length,
	rating 
FROM chinook.movie m 
WHERE rental_rate > 2
ORDER BY m.length desc
LIMIT 40)
SELECT 
	m.rating,
	min(m.length) min_length,
	max(m.length) max_length,
	avg(m.length) avg_length,
	min(m.rental_rate) min_rental_rate,
	max(m.rental_rate) max_rental_rate,
	avg(m.rental_rate) avg_rental_rate
FROM top_movies m
GROUP BY m.rating
ORDER BY avg_length;

WITH year_2012 as(
SELECT 
	EXTRACT(MONTH FROM i.invoice_date::date) month_num,
	sum(i.total) total
FROM chinook.invoice i 
WHERE EXTRACT(YEAR FROM i.invoice_date::date) = 2012
GROUP BY EXTRACT(YEAR FROM i.invoice_date::date), EXTRACT(MONTH FROM i.invoice_date::date)
),year_2013 AS (
SELECT 
	EXTRACT(MONTH FROM i.invoice_date::date) month_num,
	sum(i.total) total
FROM chinook.invoice i 
WHERE EXTRACT(YEAR FROM i.invoice_date::date) = 2013
GROUP BY EXTRACT(YEAR FROM i.invoice_date::date), EXTRACT(MONTH FROM i.invoice_date::date)
)
SELECT 
	year_2012.month_num,
	year_2012.total sum_total_2012,
	year_2013.total sum_total_2013,
	ROUND((year_2013.total - year_2012.total) * 100 / year_2012.total) as perc
FROM year_2012 
JOIN year_2013 USING(month_num)
ORDER BY year_2012.month_num;