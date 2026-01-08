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
