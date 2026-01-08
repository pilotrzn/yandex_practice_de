SELECT 
	brand.brand_name,
	EXTRACT(YEAR FROM sales.sale_date) "year",
	round(avg(s.price ),2) "price_avg"
FROM car_auto.sales sales 
JOIN car_auto.cars cars USING(car_id)
JOIN car_auto.models models USING(model_id)
JOIN car_auto.brands brand USING(brand_id)
GROUP BY EXTRACT(YEAR FROM sales.sale_date), brand.brand_name
ORDER BY 1, 2;