DROP SCHEMA IF EXISTS car_auto cascade;
CREATE SCHEMA IF NOT EXISTS car_auto;

CREATE TABLE IF NOT EXISTS car_auto.regions(
	region_id smallserial PRIMARY KEY, --выбран SMALLINT потому что количество регионов(стран) небольшое
	region_name varchar(25) NULL  -- в текущих данных максимальная длина региона - 11 символов, сделал 25 с небольшим запасом
);

CREATE TABLE IF NOT EXISTS car_auto.brands(
	brand_id smallserial PRIMARY KEY, --выбран SMALLINT потому что количество брендов небольшое
	brand_name varchar(25) NOT NULL,
	region_id SMALLINT NOT NULL CONSTRAINT brands_regions_region_id_fkey REFERENCES car_auto.regions(region_id)
);

CREATE TABLE IF NOT EXISTS car_auto.models(
	model_id smallserial PRIMARY KEY,
	model_name varchar(25) NOT NULL,
	brand_id SMALLINT NOT NULL CONSTRAINT models_brands_brand_id_fkey REFERENCES car_auto.brands(brand_id),
	gasoline_consumption numeric(3,1) NULL, -- число по условию не может быть 3 значным, а судя по самим данным - 1 знак после запятой, поэтому numerci(3,1)
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
	client_name varchar(150) NOT NULL, --выбран varchar с ограничением в 150 символов.
	phone varchar(24) NULL,
	created_at timestamp DEFAULT current_timestamp NOT NULL
	);

CREATE TABLE IF NOT EXISTS car_auto.client_discount(
	id serial PRIMARY KEY,
	client_id integer NULL CONSTRAINT client_discount_client_id_fkey REFERENCES car_auto.client(client_id),
	discount NUMERIC (5,2) NULL, -- значение скидки в процентах, максимум 3 числа и 2 после запятой
	brand_id SMALLINT NULL CONSTRAINT client_discount_brand_brand_id_fkey REFERENCES car_auto.brands(brand_id),
	created_at timestamp DEFAULT current_timestamp NOT NULL, --дата создания скидки
	modified_at timestamp DEFAULT NULL, -- дата изменения скидки
	CONSTRAINT check_discount CHECK (((discount >= (0)::numeric) AND (discount <= (100)::numeric)))
);

CREATE TABLE IF NOT EXISTS car_auto.sales(
	id serial PRIMARY KEY,
	car_id integer NOT NULL CONSTRAINT sales_car_car_id_fkey REFERENCES car_auto.cars(car_id),
	client_id integer NOT NULL CONSTRAINT sales_client_client_id_fkey REFERENCES car_auto.client(client_id),
	price numeric(9,2) NOT NULL, --цена может содержать только сотые и не может быть больше семизначной суммы. У numeric повышенная точность при работе с дробными числами, поэтому при операциях c этим типом данных, дробные числа не потеряются.
	sale_date timestamp NOT NULL 
	);