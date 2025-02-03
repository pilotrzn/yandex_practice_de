/* Создание схемы nf_lesson */
create schema nf_lesson;

/* Создание таблицы nf_lesson.preparatory_1_1nf */

DROP TABLE IF EXISTS nf_lesson.preparatory_1_1nf;
CREATE TABLE nf_lesson.preparatory_1_1nf AS
SELECT  id,
                craftsman_name,
                craftsman_address,
                customer_name,
                customer_address
FROM source1.craft_market_wide;

/* Задание первичного ключа таблицы */
ALTER TABLE nf_lesson.preparatory_1_1nf ADD CONSTRAINT pk_preparatory_1_1nf PRIMARY KEY (id);


/* Запрос */
SELECT  
	id, 
	(regexp_split_to_array(craftsman_name , '\s+'))[1] AS craftsman_name, -- имя мастера
	(regexp_split_to_array(craftsman_name , '\s+'))[2] AS craftsman_surname,
	craftsman_address ,
	(regexp_split_to_array(customer_name , '\s+'))[1] AS customer_name, -- имя мастера
	(regexp_split_to_array(customer_name , '\s+'))[2] AS customer_surname,
	customer_address 
FROM nf_lesson.preparatory_1_1nf;

/* Создание таблицы nf_lesson.preparatory_2_1nf */

DROP TABLE IF EXISTS nf_lesson.preparatory_2_1nf;
CREATE TABLE nf_lesson.preparatory_2_1nf AS
SELECT  
	id, 
	(regexp_split_to_array(craftsman_name , '\s+'))[1] AS craftsman_name, -- имя мастера
	(regexp_split_to_array(craftsman_name , '\s+'))[2] AS craftsman_surname,
	craftsman_address ,
	(regexp_split_to_array(customer_name , '\s+'))[1] AS customer_name, -- имя мастера
	(regexp_split_to_array(customer_name , '\s+'))[2] AS customer_surname,
	customer_address 
FROM nf_lesson.preparatory_1_1nf;

/* Задание первичного ключа таблицы */
ALTER TABLE nf_lesson.preparatory_2_1nf ADD CONSTRAINT pk_preparatory_2_1nf PRIMARY KEY (id);

/* Запрос */
SELECT  
	id, 
	craftsman_name, -- имя мастера
	craftsman_surname,
	(regexp_match(craftsman_address , '\d+'))[1] AS craftsman_address_building,
	(regexp_match(craftsman_address , '[a-zA-Z]+[a-zA-Z\s]+'))[1] AS craftsman_address_street,
	customer_name, -- имя мастера
	customer_surname,
	(regexp_match(customer_address , '\d+'))[1] AS customer_address_building,
	(regexp_match(customer_address , '[a-zA-Z]+[a-zA-Z\s]+'))[1] AS customer_address_street
FROM nf_lesson.preparatory_2_1nf; 

/* Создание таблицы nf_lesson.preparatory_3_1nf */

DROP TABLE IF EXISTS nf_lesson.preparatory_3_1nf;
CREATE TABLE nf_lesson.preparatory_3_1nf AS
SELECT  
	id, 
	craftsman_name, -- имя мастера
	craftsman_surname,
	(regexp_match(craftsman_address , '\d+'))[1] AS craftsman_address_building,
	(regexp_match(craftsman_address , '[a-zA-Z]+[a-zA-Z\s]+'))[1] AS craftsman_address_street,
	customer_name, -- имя мастера
	customer_surname,
	(regexp_match(customer_address , '\d+'))[1] AS customer_address_building,
	(regexp_match(customer_address , '[a-zA-Z]+[a-zA-Z\s]+'))[1] AS customer_address_street
FROM nf_lesson.preparatory_2_1nf; 

/* Задание первичного ключа таблицы */
ALTER TABLE nf_lesson.preparatory_3_1nf ADD CONSTRAINT pk_preparatory_3_1nf PRIMARY KEY (id);


/* Создание таблицы nf_lesson.craft_market_wide_1nf */

DROP TABLE IF EXISTS nf_lesson.craft_market_wide_1nf;
CREATE TABLE nf_lesson.craft_market_wide_1nf AS
SELECT 
	id, 
	craftsman_id, 
	(regexp_split_to_array(craftsman_name , '\s+'))[1] AS craftsman_name,
	(regexp_split_to_array(craftsman_name , '\s+'))[2] AS craftsman_surname,	
	(regexp_match(craftsman_address , '\d+'))[1] AS craftsman_address_building,
	(regexp_match(craftsman_address , '[a-zA-Z]+[a-zA-Z\s]+'))[1] AS craftsman_address_street,
	craftsman_birthday, 
	craftsman_email, 
	product_id, 
	product_name, 
	product_description, 
	product_type, 
	product_price, 
	order_id, 
	order_created_date, 
	order_completion_date, 
	order_status, 
	customer_id, 
	(regexp_split_to_array(customer_name , '\s+'))[1] AS customer_name, 
	(regexp_split_to_array(customer_name , '\s+'))[2] AS customer_surname,
	(regexp_match(customer_address , '\d+'))[1] AS customer_address_building,
	(regexp_match(customer_address , '[a-zA-Z]+[a-zA-Z\s]+'))[1] AS customer_address_street,
	customer_birthday, 
	customer_email
FROM source1.craft_market_wide;

ALTER TABLE nf_lesson.craft_market_wide_1nf ADD CONSTRAINT pk_craft_market_wide_1nf PRIMARY KEY (id);