/*Добавьте в этот файл все запросы, для создания схемы сafe и
 таблиц в ней в нужном порядке*/
CREATE  SCHEMA cafe;
-- drop table if exists cafe.restaurant_manager_work_dates cascade;
-- drop table if exists cafe.sales cascade;
-- drop table if exists cafe.restaurants;
-- drop table if exists cafe.managers;
-- drop type if exists cafe.restaurant_type;

CREATE TYPE  cafe.restaurant_type AS ENUM(
		'coffee_shop', 
		'restaurant', 
		'bar', 
		'pizzeria');

CREATE TABLE cafe.restaurants(
	restaurant_uuid uuid PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
	restaurant_name TEXT,
	restaurant_type cafe.restaurant_type,
	restaurant_menu jsonb
);

CREATE TABLE cafe.managers(
	manager_uuid uuid PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
	manager_name TEXT,
	manager_phone text
);

CREATE TABLE cafe.restaurant_manager_work_dates(
	restaurant_uuid uuid NOT NULL,
	manager_uuid uuid NOT NULL,
	begin_work_date date NOT NULL,
	end_work_date date NULL,
	CONSTRAINT rest_man_work_dates_rest_uuid_fkey FOREIGN KEY (restaurant_uuid) REFERENCES cafe.restaurants(restaurant_uuid),
	CONSTRAINT rest_man_work_dates_manager_uuid_fkey FOREIGN KEY (manager_uuid) REFERENCES cafe.managers(manager_uuid),
	CONSTRAINT rest_man_work_dates_pkey PRIMARY KEY (restaurant_uuid, manager_uuid)
);

CREATE TABLE cafe.sales(
	sale_date date NOT NULL,
	restaurant_uuid uuid NOT NULL,
	avg_check numeric(6,2),
	CONSTRAINT sales_sale_date_rest_uuid PRIMARY KEY(sale_date, restaurant_uuid)
	);