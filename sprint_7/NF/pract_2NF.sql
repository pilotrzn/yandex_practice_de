SELECT craftsman_id , count(*)
FROM nf_lesson.craft_market_wide_1nf cmwn 
GROUP BY craftsman_id 
HAVING count(*) > 1;

SELECT product_id , count(*)
FROM nf_lesson.craft_market_wide_1nf cmwn 
GROUP BY product_id 
HAVING count(*) > 1;

SELECT order_id , count(*)
FROM nf_lesson.craft_market_wide_1nf cmwn 
GROUP BY order_id 
HAVING count(*) > 1;

SELECT customer_id , count(*)
FROM nf_lesson.craft_market_wide_1nf cmwn 
GROUP BY customer_id 
HAVING count(*) > 1;

/*Создание таблиц nf_lesson.order_2nf*/

DROP TABLE IF EXISTS nf_lesson.order_2nf;
CREATE TABLE nf_lesson.order_2nf AS
SELECT DISTINCT 
        order_id, -- идентификатор заказа
        order_created_date, -- дата создания заказа
        order_completion_date, -- дата выполнения заказа
        order_status, -- статус выполнения заказа (created, in progress, delivery, done)
        customer_id, -- идентификатор заказчика
        customer_name, -- имя заказчика
        customer_surname, -- фамилия заказчика
        customer_address_street, -- адрес заказчика (улица)
        customer_address_building, -- адрес заказчика (номер дома)
        customer_birthday, -- дата рождения заказчика
        customer_email, -- электронная почта заказчика
        product_id -- идентификатор изделия
FROM nf_lesson.craft_market_wide_1nf; 

ALTER TABLE nf_lesson.order_2nf ADD CONSTRAINT pk_order_2nf PRIMARY KEY (order_id);

/*Создание таблиц nf_lesson.product_2nf*/

DROP TABLE IF EXISTS nf_lesson.product_2nf;
CREATE TABLE nf_lesson.product_2nf AS
SELECT DISTINCT
        product_id, -- идентификтор товара ручной работы
        product_name, -- название товара ручной работы
        product_description, -- описание товара ручной работы
        product_type, -- тип товара ручной работы
        product_price, -- цена товара ручной работы
        craftsman_id, -- идентификатор мастера
        craftsman_name, -- имя мастера
        craftsman_surname, -- фамилия мастера
        craftsman_address_street, -- адрес мастера (улица)
        craftsman_address_building, -- адрес мастера (номер дома)
        craftsman_birthday, -- дата рождения мастера
        craftsman_email -- электронная почта мастера
FROM nf_lesson.craft_market_wide_1nf; 

ALTER TABLE nf_lesson.product_2nf ADD CONSTRAINT pk_product_2nf PRIMARY KEY (product_id);