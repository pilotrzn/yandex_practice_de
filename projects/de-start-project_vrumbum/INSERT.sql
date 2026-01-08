UPDATE raw_data.sales 
SET brand_origin = 'No region' 
WHERE brand_origin IS NULL;

INSERT INTO car_auto.regions(region_name) 
SELECT DISTINCT ON (s.brand_origin) 
CASE 
	WHEN s.brand_origin IS NULL THEN 'No region'
	ELSE s.brand_origin
END
FROM raw_data.sales s
ORDER BY s.brand_origin DESC
RETURNING *;

INSERT INTO car_auto.brands (brand_name, region_id)
SELECT DISTINCT
	trim(substr(s.auto,1,strpos(split_part(s.auto, ', ',1),' '))),
	r.region_id 
FROM raw_data.sales s 
JOIN car_auto.regions r ON r.region_name = s.brand_origin 
RETURNING *;

INSERT INTO car_auto.colors (color_name)
SELECT DISTINCT 
	split_part(s.auto, ', ',2)
FROM raw_data.sales s 
RETURNING *;

INSERT INTO car_auto.models (model_name, brand_id, gasoline_consumption)
SELECT DISTINCT 
	trim(substr(split_part(s.auto, ', ',1),strpos(split_part(s.auto, ', ',1),' '))),
	b.brand_id ,
	s.gasoline_consumption 
FROM raw_data.sales s 
JOIN car_auto.brands b ON b.brand_name = substr(s.auto,1,strpos(split_part(s.auto, ', ',1),' '))
RETURNING *;

INSERT INTO car_auto.cars (model_id, color_id)
SELECT DISTINCT 
	m.model_id,
	c.color_id
FROM raw_data.sales s 
JOIN car_auto.colors c ON c.color_name = split_part(s.auto, ', ',2)
JOIN car_auto.models m ON m.model_name = substr(split_part(s.auto, ', ',1),strpos(split_part(s.auto, ', ',1),' '))
RETURNING *;

INSERT INTO car_auto.client(client_name , phone)
SELECT DISTINCT
	s.person_name,
	s.phone 
FROM  raw_data.sales s
RETURNING *;

INSERT INTO car_auto.client_discount (discount, brand_id, client_id)
SELECT s.discount ,b.brand_id, c.client_id 
FROM raw_data.sales s 
JOIN car_auto.brands b ON b.brand_name = substr(s.auto,1,strpos(split_part(s.auto, ', ',1),' '))
LEFT JOIN car_auto.client c ON c.client_name = s.person_name 
WHERE s.discount != 0
RETURNING *;

INSERT INTO car_auto.sales(car_id, client_id, price, sale_date) 
SELECT car.car_id, c.client_id, s.price ,s."date" 
FROM raw_data.sales s 
JOIN car_auto.client c ON c.client_name =s.person_name 
LEFT JOIN car_auto.models m ON m.model_name = substr(split_part(s.auto, ', ',1),strpos(split_part(s.auto, ', ',1),' '))
LEFT JOIN car_auto.colors color ON color.color_name = split_part(s.auto, ', ',2)
LEFT JOIN car_auto.cars car ON car.model_id = m.model_id AND color.color_id = car.color_id
RETURNING *;

--проверочный запрос
SELECT 
	id, 
	c.client_name, 
	c.phone,
	region.region_name ,
	b.brand_name, 
	m.model_name,
	c3.color_name,
	m.gasoline_consumption,  
	price, 
	sale_date
FROM car_auto.sales s
JOIN car_auto.client c USING(client_id)
JOIN car_auto.cars c2 USING(car_id)
JOIN car_auto.models m USING(model_id)
JOIN car_auto.brands b USING(brand_id)
JOIN car_auto.colors c3 USING(color_id)
JOIN car_auto.regions region USING(region_id)
ORDER BY 
	b.brand_name, 
	m.model_name,
	c3.color_name;
