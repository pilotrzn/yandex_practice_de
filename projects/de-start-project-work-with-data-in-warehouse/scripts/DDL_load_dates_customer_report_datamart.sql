--таблица инкрементальных загрузок

DROP TABLE IF EXISTS dwh.load_dates_customer_report_datamart;

CREATE TABLE IF NOT EXISTS dwh.load_dates_customer_report_datamart (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    load_dttm date NOT NULL,
    constraint load_dates_customer_report_datamart_pk primary key (id)
);