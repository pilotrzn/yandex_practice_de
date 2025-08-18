

DROP TABLE stg.order_events;
CREATE TABLE stg.order_events (
    id int PRIMARY KEY,  -- Суррогатный первичный ключ с автоинкрементом
    object_id int NOT NULL,  -- Идентификатор объекта в событии
    payload JSON NOT NULL,  -- Оригинальное событие в формате JSON
    object_type VARCHAR(100) NOT NULL,  -- Тип объекта для парсинга payload
    sent_dttm TIMESTAMP WITHOUT TIME ZONE NOT NULL,  -- Дата и время отправки сообщения
    CONSTRAINT order_events_object_id_unique UNIQUE (object_id)
);
-- Создание индекса для ускорения поиска по object_type
CREATE INDEX idx_order_events_object_type ON stg.order_events (object_type);
-- Создание индекса для ускорения поиска по sent_dttm
CREATE INDEX idx_order_events_sent_dttm ON stg.order_events (sent_dttm);

DROP TABLE dds.h_user;

CREATE TABLE dds.h_user(
	h_user_pk UUID PRIMARY KEY,
	user_id varchar NOT NULL,
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL 
);


CREATE TABLE dds.h_product(
	h_product_pk UUID PRIMARY KEY,
	product_id varchar NOT NULL,
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL 
);

DROP TABLE dds.h_category;
CREATE TABLE dds.h_category(
	h_category_pk UUID PRIMARY KEY,
	category_name varchar NOT NULL,
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL 
);

DROP TABLE dds.h_restaurant;
CREATE TABLE dds.h_restaurant(
	h_restaurant_pk UUID PRIMARY KEY,
	restaurant_id varchar NOT NULL,
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL 
);

DROP TABLE dds.h_order;
CREATE TABLE dds.h_order(
	h_order_pk UUID PRIMARY KEY,
	order_id int NOT NULL,
	order_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL 
);

DROP TABLE dds.l_order_product;
CREATE TABLE dds.l_order_product(
	hk_order_product_pk UUID PRIMARY KEY,
	h_order_pk UUID NOT NULL CONSTRAINT fk_l_order_product_order references dds.h_order(h_order_pk),
	h_product_pk UUID NOT NULL CONSTRAINT fk_l_order_product_product references dds.h_product(h_product_pk),
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.l_product_restaurant;
CREATE TABLE dds.l_product_restaurant(
	hk_product_restaurant_pk UUID PRIMARY KEY,
	h_restaurant_pk UUID NOT NULL CONSTRAINT fk_l_product_restaurant_restaurant references dds.h_restaurant(h_restaurant_pk),
	h_product_pk UUID NOT NULL CONSTRAINT fk_l_product_restaurant_product references dds.h_product(h_product_pk),
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.l_product_category;
CREATE TABLE dds.l_product_category(
	hk_product_category_pk UUID PRIMARY KEY,
	h_category_pk UUID NOT NULL CONSTRAINT fk_l_product_category_category references dds.h_category(h_category_pk),
	h_product_pk UUID NOT NULL CONSTRAINT fk_l_product_category_product references dds.h_product(h_product_pk),
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.l_order_user;
CREATE TABLE dds.l_order_user(
	hk_order_user_pk UUID PRIMARY KEY,
	h_order_pk UUID NOT NULL CONSTRAINT fk_l_order_user_order references dds.h_order(h_order_pk),
	h_user_pk UUID NOT NULL CONSTRAINT fk_l_order_user_user references dds.h_user(h_user_pk),
	load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL
);


DROP TABLE dds.s_user_names;
CREATE TABLE dds.s_user_names(
    h_user_pk UUID NOT NULL CONSTRAINT fk_s_user_l_users REFERENCES dds.h_user(h_user_pk),
    username varchar NOT NULL,
    userlogin varchar NOT NULL,
    load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL,
	hk_user_names_hashdiff UUID NOT NULL
);

DROP TABLE dds.s_product_names;
CREATE TABLE dds.s_product_names(
    h_product_pk UUID NOT NULL CONSTRAINT fk_s_product_l_product REFERENCES dds.h_product(h_product_pk),
    name varchar NOT NULL,
    load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL,
	hk_product_names_hashdiff UUID NOT NULL
);

DROP TABLE dds.s_restaurant_names;
CREATE TABLE dds.s_restaurant_names(
    h_restaurant_pk UUID NOT NULL CONSTRAINT fk_s_restaurant_l_restaurant REFERENCES dds.h_restaurant(h_restaurant_pk),
    name varchar NOT NULL,
    load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL,
	hk_restaurant_names_hashdiff UUID NOT NULL
);

DROP TABLE dds.s_order_cost;
CREATE TABLE dds.s_order_cost(
    h_order_pk UUID NOT NULL CONSTRAINT fk_s_order_cost_l_order REFERENCES dds.h_order(h_order_pk),
    cost decimal(19, 5) NOT NULL CHECK (cost >= 0),
    payment decimal(19, 5) NOT NULL CHECK (payment >= 0),
    load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL,
	hk_order_cost_hashdiff UUID NOT NULL
);

DROP TABLE dds.s_order_cost;
CREATE TABLE dds.s_order_cost(
    h_order_pk UUID NOT NULL CONSTRAINT fk_s_order_cost_l_order REFERENCES dds.h_order(h_order_pk),
    cost decimal(19, 5) NOT NULL CHECK (cost >= 0),
    payment decimal(19, 5) NOT NULL CHECK (payment >= 0),
    load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL,
	hk_order_cost_hashdiff UUID NOT NULL
);


DROP TABLE dds.s_order_status;
CREATE TABLE dds.s_order_status(
    hk_order_status_pk UUID NOT NULL CONSTRAINT fk_s_order_cost_unique UNIQUE(h_order_pk, load_dt),
    h_order_pk UUID NOT NULL CONSTRAINT fk_s_order_status_l_order REFERENCES dds.h_order(h_order_pk),
    status VARCHAR not null,
    load_dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	load_src varchar NOT NULL,
	hk_order_status_hashdiff UUID NOT NULL
);

