# Проект Врум-Бум!. Схема магазина авто

```sql
-- создается схема
DROP SCHEMA IF EXISTS car_auto cascade;
CREATE SCHEMA IF NOT EXISTS car_auto;

CREATE TABLE IF NOT EXISTS car_auto.regions(
	region_id smallserial PRIMARY KEY,
	region_name varchar(25) NULL
);

CREATE TABLE IF NOT EXISTS car_auto.brands(
	brand_id smallserial PRIMARY KEY,
	brand_name varchar(25) NOT NULL,
	region_id SMALLINT NOT NULL CONSTRAINT brands_regions_region_id_fkey REFERENCES car_auto.regions(region_id)
);

CREATE TABLE IF NOT EXISTS car_auto.models(
	model_id smallserial PRIMARY KEY,
	model_name varchar(25) NOT NULL,
	brand_id SMALLINT NOT NULL CONSTRAINT models_brands_brand_id_fkey REFERENCES car_auto.brands(brand_id),
	gasoline_consumption numeric(3,1) NULL,
	created_at timestamp DEFAULT current_timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS car_auto.colors(
	color_id smallserial PRIMARY KEY,
	color_name varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS car_auto.cars(
	car_id serial PRIMARY KEY,
	model_id SMALLINT NOT NULL CONSTRAINT car_models_models_model_id_fkey REFERENCES car_auto.models(model_id),
	color_id SMALLINT NOT NULL CONSTRAINT cars_colors_color_id_fkey REFERENCES car_auto.colors(color_id), 
	created_at timestamp DEFAULT current_timestamp NOT NULL 
);

CREATE TABLE IF NOT EXISTS car_auto.client(
	client_id serial PRIMARY KEY,
	client_name varchar(150) NOT NULL,
	phone varchar(24) NULL,
	created_at timestamp DEFAULT current_timestamp NOT NULL
	);

CREATE TABLE IF NOT EXISTS car_auto.client_discount(
	id serial PRIMARY KEY,
	client_id integer NULL,
	discount NUMERIC (5,2) NULL,
	brand_id SMALLINT NULL CONSTRAINT client_discount_brand_brand_id_fkey REFERENCES car_auto.brands(brand_id),
	created_at timestamp DEFAULT current_timestamp NOT NULL,
	modified_at timestamp DEFAULT NULL,
	CONSTRAINT client_discount_client_id_fkey FOREIGN KEY (client_id) REFERENCES  car_auto.client(client_id)	
);

CREATE TABLE IF NOT EXISTS car_auto.sales(
	id serial PRIMARY KEY,
	car_id integer NOT NULL CONSTRAINT sales_car_car_id_fkey REFERENCES car_auto.cars(car_id),
	client_id integer NOT NULL CONSTRAINT sales_client_client_id_fkey REFERENCES car_auto.client(client_id),
	price numeric(9,2) NOT NULL,
	sale_date timestamp NOT NULL
	);
```


```sql
UPDATE raw_data.sales 
SET brand_origin = 'No region' 
WHERE brand_origin IS NULL;

TRUNCATE TABLE car_auto.regions RESTART IDENTITY cascade;

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

--TRUNCATE TABLE car_auto.client RESTART IDENTITY cascade;
INSERT INTO car_auto.client(client_name , phone)
SELECT DISTINCT
	s.person_name,
	s.phone 
FROM  raw_data.sales s
RETURNING *;

--TRUNCATE TABLE car_auto.client_discount RESTART IDENTITY cascade;
INSERT INTO car_auto.client_discount (discount, brand_id, client_id)
SELECT s.discount ,b.brand_id, c.client_id 
FROM raw_data.sales s 
JOIN car_auto.brands b ON b.brand_name = substr(s.auto,1,strpos(split_part(s.auto, ', ',1),' '))
LEFT JOIN car_auto.client c ON c.client_name = s.person_name 
WHERE s.discount != 0
RETURNING *;

TRUNCATE TABLE car_auto.sales RESTART IDENTITY cascade;
INSERT INTO car_auto.sales(car_id, client_id, price, sale_date) 
SELECT car.car_id, c.client_id, s.price ,s."date" 
FROM raw_data.sales s 
JOIN car_auto.client c ON c.client_name =s.person_name 
LEFT JOIN car_auto.models m ON m.model_name = substr(split_part(s.auto, ', ',1),strpos(split_part(s.auto, ', ',1),' '))
LEFT JOIN car_auto.colors color ON color.color_name = split_part(s.auto, ', ',2)
LEFT JOIN car_auto.cars car ON car.model_id = m.model_id AND color.color_id = car.color_id
RETURNING *;
```