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
GROUP BY region.region_name;
