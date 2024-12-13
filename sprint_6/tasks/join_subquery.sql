EXPLAIN analyze
 SELECT 
 	res.month_num,
 	sum(CASE WHEN res.year_num = 2011 THEN res.invoices	END) year_2011,
 	sum(CASE WHEN res.year_num = 2012 THEN res.invoices	END) year_2012,
 	sum(CASE WHEN res.year_num = 2013 THEN res.invoices	END) year_2013
 FROM (  
		 SELECT count(*) invoices,
		 	EXTRACT(MONTH FROM i.invoice_date::date) month_num,
		 	EXTRACT(YEAR FROM i.invoice_date::date) year_num
 		FROM chinook.invoice i
 		WHERE EXTRACT(YEAR FROM i.invoice_date::date) BETWEEN 2011 AND 2013
 		GROUP BY EXTRACT(MONTH FROM i.invoice_date::date),EXTRACT(YEAR FROM i.invoice_date::date)) res
 GROUP BY res.month_num;
 
EXPLAIN analyze
SELECT 
	year_2011.month_num invoice_month,
	year_2011.invoices year_2011,
	year_2012.invoices year_2012,
	year_2013.invoices year_2013
FROM (
		SELECT 
			count(*) invoices,
		 	EXTRACT(MONTH FROM i.invoice_date::date) month_num
		FROM chinook.invoice i
		WHERE EXTRACT(YEAR FROM i.invoice_date::date) = 2011
		GROUP BY EXTRACT(MONTH FROM i.invoice_date::date)) year_2011
LEFT JOIN (
			SELECT 
				count(*) invoices,
		 		EXTRACT(MONTH FROM i.invoice_date::date) month_num
			FROM chinook.invoice i
			WHERE EXTRACT(YEAR FROM i.invoice_date::date) = 2012
			GROUP BY EXTRACT(MONTH FROM i.invoice_date::date)) year_2012
ON year_2011.month_num = year_2012.month_num
LEFT JOIN (
			SELECT 
				count(*) invoices,
		 		EXTRACT(MONTH FROM i.invoice_date::date) month_num
			FROM chinook.invoice i
			WHERE EXTRACT(YEAR FROM i.invoice_date::date) = 2013
			GROUP BY EXTRACT(MONTH FROM i.invoice_date::date)) year_2013
ON year_2011.month_num = year_2013.month_num;

SELECT DISTINCT c.last_name 
FROM chinook.client c 
WHERE c.customer_id  IN (
	SELECT wo_jan.customer_id wo
	FROM (
		SELECT DISTINCT customer_id 
		FROM chinook.invoice i 
		WHERE i.invoice_date BETWEEN '2013-02-01'AND '2013-12-31') wo_jan
	LEFT JOIN (
		SELECT DISTINCT customer_id 
		FROM chinook.invoice i 
		WHERE i.invoice_date BETWEEN '2013-01-01'AND '2013-01-31') jan
		USING(customer_id)
	WHERE jan.customer_id IS NOT NULL
);

EXPLAIN ANALYZE 
SELECT 
	t.name name_category,
	count(1) total_films
FROM (
	SELECT DISTINCT m.film_id ,c."name" 
	FROM chinook.movie m 
	JOIN chinook.film_actor fa USING (film_id)
	JOIN chinook.film_category fc USING(film_id)
	JOIN chinook.category c USING(category_id)
	JOIN (
		SELECT fa.actor_id
		FROM chinook.movie m
		JOIN chinook.film_actor fa USING (film_id)
		WHERE m.release_year > 2013
		GROUP BY fa.actor_id
		HAVING count(1) > 7) actors
	ON actors.actor_id = fa.actor_id ) t
GROUP BY t.name
ORDER BY total_films DESC, name_category;

EXPLAIN ANALYZE 
SELECT 
	t.name name_category,
	count(1) total_films
FROM (
	SELECT DISTINCT m.film_id ,c."name" 
	FROM chinook.movie m 
	JOIN chinook.film_actor fa USING (film_id)
	JOIN chinook.film_category fc USING(film_id)
	JOIN chinook.category c USING(category_id)
	WHERE fa.actor_id in (
				SELECT fa.actor_id
				FROM chinook.movie m
				JOIN chinook.film_actor fa USING (film_id)
				WHERE m.release_year > 2013
				GROUP BY fa.actor_id
				HAVING count(*) > 7)
		) t
GROUP BY t.name
ORDER BY total_films DESC, name_category


SELECT 
	c.name AS name_category, 
	COUNT(DISTINCT fc.film_id) AS total_films
FROM chinook.category AS c
JOIN chinook.film_category AS fc ON fc.category_id = c.category_id
JOIN chinook.film_actor AS fa ON fc.film_id = fa.film_id
WHERE fa.actor_id IN (
			SELECT fa.actor_id
			FROM chinook.film_actor AS fa
			LEFT JOIN chinook.movie AS m ON fa.film_id = m.film_id
			WHERE m.release_year > 2013
			GROUP BY fa.actor_id
			HAVING COUNT(fa.film_id) > 7)
GROUP BY name_category
ORDER BY total_films DESC, name_category;