
```sql
--
SELECT round(CAST(100 * (count(*) - count(m.gasoline_consumption))::real/count(*) AS NUMERIC), 2) nulls_percentage_gasoline_consumption
FROM car_auto.models m ;

--
SELECT 
	brand.brand_name,
	EXTRACT(YEAR FROM s.sale_date) "year",
	round(avg(s.price ),2) "price_avg"
FROM car_auto.sales s 
JOIN car_auto.cars cars USING(car_id)
JOIN car_auto.models models USING(model_id)
JOIN car_auto.brands brand USING(brand_id)
GROUP BY EXTRACT(YEAR FROM s.sale_date),brand.brand_name
ORDER BY 1, 2;


SELECT 
	EXTRACT(MONTH FROM sales.sale_date) "month", 
	EXTRACT(YEAR FROM sales.sale_date) "year", 
	round(avg(sales.price ),2) "price_avg"
FROM car_auto.sales sales 
WHERE EXTRACT(YEAR FROM sales.sale_date) = 2022
GROUP BY EXTRACT(MONTH FROM sales.sale_date),EXTRACT(YEAR FROM sales.sale_date)
ORDER BY 1;


SELECT 
    client.client_name person,
    string_agg(concat(brand.brand_name, ' ', model.model_name),', ') cars
FROM car_auto.sales s 
JOIN car_auto.cars cars USING(car_id)
JOIN car_auto.client client USING(client_id)
JOIN car_auto.models model USING(model_id)
JOIN car_auto.brands brand USING(brand_id)
GROUP BY client.client_name
ORDER BY 1;

SELECT 
    region.region_name, 
    round(max((100 * sales.price)/(100 - COALESCE(cd.discount , 0))),2) price_max,
    round(min((100 * sales.price)/(100 - COALESCE(cd.discount , 0))),2) price_min
FROM car_auto.sales sales
JOIN car_auto.cars cars USING(car_id)
JOIN car_auto.models model USING(model_id)
JOIN car_auto.brands brand USING(brand_id)
JOIN car_auto.regions region USING(region_id)
LEFT JOIN car_auto.client_discount cd USING(client_id)
GROUP BY region.region_name ;

SELECT count(*) persons_from_usa_count
FROM car_auto.client c 
WHERE c.phone LIKE '+1%';

```