DROP TABLE IF EXISTS model_lesson.d_product;
CREATE TABLE model_lesson.d_product (
    product_id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL,
  	product_name text NOT NULL                                           
); 

DROP TABLE IF EXISTS model_lesson.d_shop;
CREATE TABLE model_lesson.d_shop (
  shop_id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL,
  shop_name TEXT NOT NULL,
  shop_address json NOT null
);

DROP TABLE IF EXISTS model_lesson.d_customer;
CREATE TABLE model_lesson.d_customer (
  customer_id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL,
  customer_name TEXT NOT NULL,
  customer_phone_number TEXT NOT NULL,
  customer_address json NOT NULL 
);


DROP TABLE IF EXISTS model_lesson.f_order;
CREATE TABLE model_lesson.f_order (
    order_id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL,
    create_dttm timestamp NOT NULL,
    shop_id bigint NOT NULL,
    product_id bigint NOT NULL ,
    item_count int NOT NULL,
    customer_id bigint NOT NULL,
    order_status TEXT NOT NULL,
  CONSTRAINT fk_product FOREIGN KEY(product_id) REFERENCES model_lesson.d_product(product_id),
  CONSTRAINT fk_shop FOREIGN KEY(shop_id) REFERENCES model_lesson.d_shop(shop_id),
  CONSTRAINT fk_customer FOREIGN KEY(customer_id) REFERENCES model_lesson.d_customer(customer_id)
); 

DROP TABLE IF EXISTS model_lesson.d_address;
CREATE TABLE model_lesson.d_address (
	address_id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL,
 	address_json json NOT NULL,
  	city TEXT NOT NULL,
  	street TEXT NOT NULL,
  	house TEXT NOT NULL,
  	post_index TEXT NOT NULL
);

ALTER TABLE model_lesson.d_shop RENAME COLUMN shop_address TO shop_address_id;
ALTER TABLE model_lesson.d_shop ALTER COLUMN shop_address_id TYPE bigint USING NULL;
ALTER TABLE model_lesson.d_shop ADD FOREIGN KEY (shop_address_id) REFERENCES model_lesson.d_address(address_id); 
ALTER TABLE model_lesson.d_customer RENAME COLUMN customer_address TO customer_address_id;
ALTER TABLE model_lesson.d_customer ALTER COLUMN customer_address_id TYPE bigint USING NULL;
ALTER TABLE model_lesson.d_customer ADD FOREIGN KEY (customer_address_id) REFERENCES model_lesson.d_address(address_id); 

INSERT INTO model_lesson.d_address (address_json,city, street, house, post_index)
SELECT
   customer_address::jsonb AS address_json,
  (customer_address ->> 'cityName')::text AS city,
  (customer_address ->> 'street')::text AS street,
  (customer_address ->> 'house')::text AS house,
  (customer_address ->> 'postIndex')::text AS post_index
FROM source4.ORDER
UNION ALL
SELECT
   shop_address::jsonb AS address_json,
  (shop_address ->> 'cityName')::text AS city,
  (shop_address ->> 'street')::text AS street,
  (shop_address ->> 'house')::text AS house,
  (shop_address ->> 'postIndex')::text AS post_index
FROM source4.ORDER;

INSERT INTO model_lesson.d_product (product_name)
SELECT DISTINCT product_name
FROM source4."order";

INSERT INTO model_lesson.d_shop
(shop_name, shop_address_id)
SELECT DISTINCT o.shop_name, a.address_id 
FROM source4."order" o 
JOIN model_lesson.d_address a ON a.address_json::text = o.shop_address::text;

INSERT INTO model_lesson.d_customer (customer_name, customer_phone_number, customer_address_id)
SELECT DISTINCT
    o.customer_name,
    o.customer_phone_number,
    a.address_id AS customer_address_id
FROM source4.order o
JOIN model_lesson.d_address a ON o.customer_address::text= a.address_json::text;

INSERT INTO model_lesson.f_order (create_dttm, shop_id, product_id, item_count, customer_id, order_status)
SELECT o.create_dttm, s.shop_id, p.product_id, o.item_count, c.customer_id, o.order_status
FROM source4.order o
  JOIN model_lesson.d_address shop_a ON o.shop_address::text = shop_a.address_json::text
  JOIN model_lesson.d_address customer_a ON o.customer_address::text = customer_a.address_json::text
  JOIN model_lesson.d_product p ON o.product_name = p.product_name
  JOIN model_lesson.d_shop s ON o.shop_name = s.shop_name AND shop_a.address_id = s.shop_address_id
  JOIN model_lesson.d_customer c ON o.customer_name = c.customer_name AND o.customer_phone_number = c.customer_phone_number AND customer_a.address_id = c.customer_address_id; 