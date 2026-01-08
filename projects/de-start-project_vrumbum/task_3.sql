SELECT 
	EXTRACT(MONTH FROM sales.sale_date) "month", 
	EXTRACT(YEAR FROM sales.sale_date) "year", 
	round(avg(sales.price ),2) "price_avg"
FROM car_auto.sales sales 
WHERE EXTRACT(YEAR FROM sales.sale_date) = 2022
GROUP BY EXTRACT(MONTH FROM sales.sale_date), EXTRACT(YEAR FROM sales.sale_date)
ORDER BY 1;
