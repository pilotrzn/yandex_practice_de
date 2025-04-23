
drop table if exists  mart.f_research;
drop table if exists  mart.f_daily_sales;
drop table if exists  mart.f_activity;
drop table if exists  mart.d_calendar;
drop table if exists  mart.d_category;
drop table if exists  mart.d_item;
drop table if exists  mart.d_customer;
drop table if exists  mart.d_city;









CREATE TABLE mart.d_customer(
   id               SERIAL   NOT NULL    ,
   customer_id      INT PRIMARY KEY,
   first_name       varchar(15),
   last_name        varchar(15),
   city_id          INT
);
CREATE INDEX d_cust1  ON mart.d_customer (customer_id);

CREATE TABLE mart.d_city(
   id               SERIAL      PRIMARY KEY,
   city_id          INT,
   city_name        varchar(50)
);
CREATE INDEX d_city1  ON mart.d_city (city_id);

CREATE TABLE mart.d_item(
   id               SERIAL      NOT NULL,
   item_id          INT         PRIMARY KEY,
   item_name        varchar(50),
   category_id      INT         NOT NULL
);
CREATE INDEX d_item1  ON mart.d_item (item_id);

CREATE TABLE mart.d_category(
   id               SERIAL      PRIMARY KEY,
   category_id      INT         NOT NULL,
   category_name    VARCHAR(50)
);
CREATE INDEX d_category1  ON mart.d_category (category_id);

CREATE TABLE mart.d_calendar(
   date_id          INT         PRIMARY KEY,
   day_num          INT,
   month_num        INT,
   month_name       VARCHAR(8),
   year_num         INT
);
CREATE INDEX d_calendar1  ON mart.d_calendar (year_num);

CREATE TABLE mart.f_activity(
   activity_id      INT NOT NULL,
   date_id          INT NOT NULL,
   click_number     INT,
   PRIMARY KEY (activity_id, date_id),
   FOREIGN KEY (date_id) REFERENCES mart.d_calendar(date_id) ON UPDATE CASCADE
);
CREATE INDEX f_activity1  ON mart.f_activity (date_id);
CREATE INDEX f_activity2  ON mart.f_activity (activity_id);

CREATE TABLE mart.f_daily_sales(
   date_id          INT NOT NULL,
   item_id          INT NOT NULL,
   customer_id      INT NOT NULL,
   price            decimal(10,2), --цена из прайс листа
   quantity         BIGINT,
   payment_amount   DECIMAL(10,2),
   PRIMARY KEY (date_id, item_id, customer_id),
   FOREIGN KEY (date_id) REFERENCES mart.d_calendar(date_id) ON UPDATE CASCADE,
   FOREIGN KEY (item_id) REFERENCES mart.d_item(item_id) ON UPDATE CASCADE,
   FOREIGN KEY (customer_id) REFERENCES mart.d_customer(customer_id) ON UPDATE CASCADE
);
CREATE INDEX f_ds1  ON mart.f_daily_sales (date_id);
CREATE INDEX f_ds2  ON mart.f_daily_sales (item_id);
CREATE INDEX f_ds3  ON mart.f_daily_sales (customer_id);

CREATE TABLE mart.f_research(
   date_id          INT NOT NULL,
   category_id      INT NOT NULL,
   geo_id           INT NOT NULL,
   customer_id      INT NOT NULL,
   item_id          INT NOT NULL,
   quantity         BIGINT,
   amount           DECIMAL(10,2),
   PRIMARY KEY (date_id, category_id, geo_id),
   FOREIGN KEY (date_id) REFERENCES mart.d_calendar(date_id) ON UPDATE CASCADE,
   FOREIGN KEY (item_id) REFERENCES mart.d_item(item_id) ON UPDATE CASCADE,
   FOREIGN KEY (customer_id) REFERENCES mart.d_customer(customer_id) ON UPDATE CASCADE
);
CREATE INDEX f_r1  ON mart.f_daily_sales (date_id);
CREATE INDEX f_r2  ON mart.f_daily_sales (item_id);
CREATE INDEX f_r3  ON mart.f_daily_sales (customer_id);


