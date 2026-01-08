DROP TABLE IF EXISTS dwh.customer_report_datamart;

CREATE TABLE dwh.customer_report_datamart (
    id int8 GENERATED ALWAYS AS IDENTITY NOT NULL, -- идентификатор записи;
    customer_id int8 NOT NULL, -- идентификатор заказчика;
    customer_name varchar NOT NULL, -- Ф. И. О. заказчика;
    customer_address varchar NOT NULL, -- адрес заказчика;
    customer_birthday date NOT NULL, -- дата рождения заказчика;
    customer_email varchar NOT NULL, -- электронная почта заказчика;
    customer_money numeric(15, 2) NOT NULL, -- сумма, которую потратил заказчик;
    platform_money int8 NOT NULL, -- сумма, которую заработала платформа от покупок заказчика за месяц (10% от суммы, которую потратил заказчик)
    count_order int8 NOT NULL, -- количество заказов у заказчика за месяц;
    avg_price_order numeric(10, 2) NOT NULL, -- средняя стоимость одного заказа у заказчика за месяц; 
    median_time_order_completed numeric(10, 1) NULL, -- медианное время в днях от момента создания заказа до его завершения за месяц;
    top_product_category varchar NOT NULL, -- самая популярная категория товаров у этого заказчика за месяц;
    top_craftsman_id int8 not null, -- идентификатор самого популярного мастера ручной работы у заказчика.
    count_order_created int8 NOT NULL, -- количество созданных заказов за месяц;
    count_order_in_progress int8 NOT NULL, -- количество заказов в процессе изготовки за месяц;
    count_order_delivery int8 NOT NULL, -- количество заказов в доставке за месяц;
    count_order_done int8 NOT NULL, -- количество завершённых заказов за месяц;
    count_order_not_done int8 NOT NULL, -- количество незавершённых заказов за месяц;
    report_period varchar NOT NULL, -- отчётный период, год и месяц.
    CONSTRAINT customer_report_datamart_pk PRIMARY KEY (id)
);