CREATE TABLE IF NOT EXISTS cdm.dm_courier_ledger(
	id int GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
	courier_id int NOT NULL,
	courier_name varchar NOT NULL,
	settlement_year int NOT NULL CHECK (settlement_year >= 2022 AND settlement_year < 2500), 
	settlement_month int NOT NULL CHECK(settlement_month >= 1 and settlement_month <= 12),
	orders_count int NOT NULL DEFAULT 0 CHECK (orders_count >= 0),
	orders_total_sum NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (orders_total_sum >= 0),
	rate_avg NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (rate_avg >= 0),
	order_processing_fee NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (order_processing_fee >= 0),
	courier_order_sum NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (courier_order_sum >= 0),
	courier_tips_sum NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (courier_tips_sum >= 0),
	courier_reward_sum NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (courier_reward_sum >= 0),
	CONSTRAINT dm_courier_ledger_unique UNIQUE (courier_id, settlement_year, settlement_month)
);

CREATE TABLE IF NOT EXISTS stg.deliverysystem_restaurants(
    object_id varchar NOT NULL,
    object_value varchar NOT NULL,
    CONSTRAINT deliverysystem_restaurants_restaurant_id_unique UNIQUE (object_id)
);

CREATE TABLE IF NOT EXISTS stg.deliverysystem_couriers(
	id serial primary key,
    object_id varchar NOT NULL,
	object_value varchar NOT NULL,
    CONSTRAINT deliverysystem_couriers_courier_id_unique UNIQUE (object_id)
);

CREATE TABLE IF NOT EXISTS stg.deliverysystem_deliveries(
    id serial,
    delivery_id varchar NOT NULL,
    delivery_value varchar NOT NULL,
    CONSTRAINT deliverysystem_deliveries_order_id_unique UNIQUE (delivery_id)
);


CREATE TABLE IF NOT EXISTS dds.dm_couriers(
	id serial PRIMARY KEY,
	courier_id varchar UNIQUE NOT NULL,
	courier_name varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dm_delivery_timestamps
(
	id serial PRIMARY KEY,
	ts timestamp UNIQUE NOT NULL,
	year smallint NOT NULL CONSTRAINT dm_dlvr_timestamps_year_check CHECK ((year >= 2022) and (year < 2500)),
	month smallint NOT NULL CONSTRAINT dm_dlvr_timestamps_month_check CHECK ((month >= 1) and (month <= 12)),
	day smallint NOT NULL CONSTRAINT dm_dlvr_timestamps_day_check CHECK ((day >= 1) and (day <= 31)),
	time time NOT NULL,
	date date NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dm_deliveries(
    id serial PRIMARY KEY,
    delivery_id varchar NOT NULL CONSTRAINT dm_deliveries_delivery_id_check UNIQUE ,
    courier_id int NOT NULL CONSTRAINT dm_deliveries_courier_id_fkey REFERENCES dds.dm_couriers(id),
    delivery_ts_id int NOT NULL CONSTRAINT dm_deliveries_ts_id_fkey REFERENCES dds.dm_delivery_timestamps(id),
    address varchar NOT NULL
);

CREATE TABLE dds.fct_deliveries(
	id serial PRIMARY KEY,
	delivery_id int NOT NULL CONSTRAINT fct_deliveries_id_fkey REFERENCES dds.dm_deliveries(id),
	order_id int NOT NULL CONSTRAINT fct_deliveries_order_id_fkey REFERENCES dds.dm_orders(id),
	sum numeric(14,2) NOT NULL DEFAULT 0 CONSTRAINT fct_deliveries_sum_check CHECK (sum >= 0),
	tip_sum numeric(14,2) NOT NULL DEFAULT 0 CONSTRAINT fct_deliveries_tip_sum_check CHECK (tip_sum >= 0),
	rate int NOT NULL DEFAULT 0 CONSTRAINT fct_deliveries_rate_check CHECK (rate >= 0),
	CONSTRAINT fct_deliveries_delivery_id_order_id_unique UNIQUE (delivery_id, order_id)
);