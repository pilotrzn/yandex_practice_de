/*Создание таблицы nf_lesson.order_3nf*/

DROP TABLE IF EXISTS nf_lesson.order_3nf;
CREATE TABLE nf_lesson.order_3nf AS
SELECT DISTINCT 
        order_id, -- идентификатор заказа
        order_created_date, -- дата создания заказа
        order_completion_date, -- дата выполнения заказа
        order_status, -- статус выполнения заказа (created, in progress, delivery, done)
        customer_id, -- идентификатор заказчика
        product_id -- идентификатор изделия
FROM nf_lesson.order_2nf;

ALTER TABLE nf_lesson.order_3nf ADD CONSTRAINT pk_order_3nf PRIMARY KEY (order_id);

/*Создание таблицы nf_lesson.customer_3nf*/

DROP TABLE IF EXISTS nf_lesson.customer_3nf;
CREATE TABLE nf_lesson.customer_3nf AS
SELECT DISTINCT 
	customer_id, 
	customer_name, 
	customer_surname, 
	customer_address_street, 
	customer_address_building, 
	customer_birthday, 
	customer_email
FROM nf_lesson.order_2nf;

ALTER TABLE nf_lesson.customer_3nf ADD CONSTRAINT pk_customer_3nf PRIMARY KEY (customer_id);

/*Создание таблиц nf_lesson.product_3nf*/

DROP TABLE IF EXISTS nf_lesson.product_3nf;
CREATE TABLE nf_lesson.product_3nf AS
SELECT DISTINCT 
product_id, 
product_name, 
product_description, 
product_type, 
product_price
FROM nf_lesson.product_2nf;

ALTER TABLE nf_lesson.product_3nf ADD CONSTRAINT pk_product_3nf PRIMARY KEY (product_id);

/*Создание таблиц nf_lesson.craftsman_3nf*/

DROP TABLE IF EXISTS nf_lesson.craftsman_3nf;
CREATE TABLE nf_lesson.craftsman_3nf AS
SELECT DISTINCT
	craftsman_id, 
	craftsman_name, 
	craftsman_surname, 
	craftsman_address_street, 
	craftsman_address_building, 
	craftsman_birthday,
	craftsman_email
FROM nf_lesson.product_2nf;

ALTER TABLE nf_lesson.craftsman_3nf ADD CONSTRAINT pk_craftsman_3nf PRIMARY KEY (craftsman_id);