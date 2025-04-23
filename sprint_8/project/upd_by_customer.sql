WITH
    dwh_delta as (
        SELECT
            dcs.customer_id,
            dcs.customer_name,
            dcs.customer_address,
            dcs.customer_birthday,
            dcs.customer_email,
            dc.craftsman_id,
            fo.order_id,
            dp.product_id,
            dp.product_price,
            dp.product_type,
            fo.order_completion_date - fo.order_created_date diff_order_date,
            fo.order_status,
            to_char (
                fo.order_created_date,
                'yyyy-mm'
            ) report_period,
            crd.id exist_customer_id,
            dcs.load_dttm craftsman_load_dttm,
            dcs.load_dttm customers_load_dttm,
            dp.load_dttm products_load_dttm
        FROM
            dwh.f_order fo
            INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id = dc.craftsman_id
            INNER JOIN dwh.d_customer dcs ON fo.customer_id = dcs.customer_id
            INNER JOIN dwh.d_product dp ON dp.product_id = fo.product_id
            LEFT JOIN dwh.load_dates_customer_report_datamart crd ON crd.id = dcs.customer_id
        WHERE (
                fo.load_dttm > (
                    SELECT COALESCE(MAX(load_dttm), '1900-01-01')
                    FROM dwh.load_dates_customer_report_datamart
                )
            )
            OR (
                dc.load_dttm > (
                    SELECT COALESCE(MAX(load_dttm), '1900-01-01')
                    FROM dwh.load_dates_customer_report_datamart
                )
            )
            OR (
                dcs.load_dttm > (
                    SELECT COALESCE(MAX(load_dttm), '1900-01-01')
                    FROM dwh.load_dates_customer_report_datamart
                )
            )
            OR (
                dp.load_dttm > (
                    SELECT COALESCE(MAX(load_dttm), '1900-01-01')
                    FROM dwh.load_dates_customer_report_datamart
                )
            )
    ),
    dwh_update_delta as (
        SELECT dd.customer_id
        FROM dwh_delta dd
        WHERE
            dd.exist_customer_id IS NOT NULL
    ),
    dwh_delta_insert_result AS (
        SELECT
            aggr.customer_id,
            aggr.customer_name,
            aggr.customer_address,
            aggr.customer_birthday,
            aggr.customer_email,
            aggr.customer_money,
            aggr.platform_money,
            aggr.count_order,
            aggr.avg_price_order,
            aggr.median_time_order_completed,
            top_product.product_type top_product_category,
            top_craftsman.top_craftsman_id,
            aggr.count_order_created,
            aggr.count_order_in_progress,
            aggr.count_order_delivery,
            aggr.count_order_done,
            aggr.count_order_not_done,
            aggr.report_period
        FROM (
                SELECT
                    dd.customer_id,
                    dd.customer_name,
                    dd.customer_address,
                    dd.customer_birthday,
                    dd.customer_email,
                    sum(dd.product_price) * 0.9 customer_money,
                    sum(dd.product_price) * 0.1 platform_money,
                    count(dd.order_id) count_order,
                    avg(dd.product_price) avg_price_order,
                    percentile_cont (0.5) WITHIN GROUP (
                        ORDER BY dd.diff_order_date
                    ) median_time_order_completed,
                    sum(
                        CASE
                            WHEN dd.order_status = 'created' THEN 1
                            ELSE 0
                        END
                    ) count_order_created,
                    sum(
                        CASE
                            WHEN dd.order_status = 'in progress' THEN 1
                            ELSE 0
                        END
                    ) count_order_in_progress,
                    sum(
                        CASE
                            WHEN dd.order_status = 'delivery' THEN 1
                            ELSE 0
                        END
                    ) count_order_delivery,
                    sum(
                        CASE
                            WHEN dd.order_status = 'done' THEN 1
                            ELSE 0
                        END
                    ) count_order_done,
                    sum(
                        CASE
                            WHEN dd.order_status != 'done' THEN 1
                            ELSE 0
                        END
                    ) count_order_not_done,
                    dd.report_period
                FROM dwh_delta AS dd
                WHERE
                    dd.exist_customer_id IS NULL
                GROUP BY
                    dd.customer_id,
                    dd.customer_name,
                    dd.customer_address,
                    dd.customer_birthday,
                    dd.customer_email,
                    dd.report_period
            ) aggr
            INNER JOIN (
                SELECT
                    dd.customer_id customer_id,
                    dd.craftsman_id top_craftsman_id,
                    count(dd.order_id) count_order,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            dd.customer_id
                        ORDER BY count(dd.order_id), count(dd.order_id) DESC
                    ) rank_count
                FROM dwh_delta dd
                GROUP BY
                    dd.customer_id,
                    dd.craftsman_id
            ) top_craftsman ON aggr.customer_id = top_craftsman.customer_id
            AND top_craftsman.rank_count = 1
            INNER JOIN (
                SELECT
                    dd.customer_id customer_id,
                    dd.product_type,
                    count(product_id) count_product,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            dd.customer_id
                        ORDER BY dd.product_type, count(product_id) DESC
                    ) rank_count
                FROM dwh_delta dd
                GROUP BY
                    dd.customer_id,
                    dd.product_type
            ) AS top_product ON aggr.customer_id = top_product.customer_id
            AND top_product.rank_count = 1
    ),
    dwh_delta_update_result AS (
        SELECT
            aggr.customer_id,
            aggr.customer_name,
            aggr.customer_address,
            aggr.customer_birthday,
            aggr.customer_email,
            aggr.customer_money,
            aggr.platform_money,
            aggr.count_order,
            aggr.avg_price_order,
            aggr.median_time_order_completed,
            top_product.product_type top_product_category,
            top_craftsman.top_craftsman_id top_craftsman_id,
            aggr.count_order_created,
            aggr.count_order_in_progress,
            aggr.count_order_delivery,
            aggr.count_order_done,
            aggr.count_order_not_done,
            aggr.report_period
        FROM (
                SELECT
                    customers.customer_id,
                    customers.customer_name,
                    customers.customer_address,
                    customers.customer_birthday,
                    customers.customer_email,
                    sum(customers.product_price) * 0.9 customer_money,
                    sum(customers.product_price) * 0.1 platform_money,
                    count(customers.order_id) count_order,
                    avg(customers.product_price) avg_price_order,
                    percentile_cont (0.5) WITHIN GROUP (
                        ORDER BY customers.diff_order_date
                    ) median_time_order_completed,
                    sum(
                        CASE
                            WHEN customers.order_status = 'created' THEN 1
                            ELSE 0
                        END
                    ) count_order_created,
                    sum(
                        CASE
                            WHEN customers.order_status = 'in progress' THEN 1
                            ELSE 0
                        END
                    ) count_order_in_progress,
                    sum(
                        CASE
                            WHEN customers.order_status = 'delivery' THEN 1
                            ELSE 0
                        END
                    ) count_order_delivery,
                    sum(
                        CASE
                            WHEN customers.order_status = 'done' THEN 1
                            ELSE 0
                        END
                    ) count_order_done,
                    sum(
                        CASE
                            WHEN customers.order_status != 'done' THEN 1
                            ELSE 0
                        END
                    ) count_order_not_done,
                    customers.report_period
                FROM (
                        SELECT
                            dcs.customer_id, dcs.customer_name, dcs.customer_address, dcs.customer_birthday, dcs.customer_email, fo.order_id, dp.product_id, dp.product_price, dp.product_type, fo.order_completion_date - fo.order_created_date diff_order_date, fo.order_status, to_char (
                                fo.order_created_date, 'yyyy-mm'
                            ) report_period, dcs.load_dttm craftsman_load_dttm, dcs.load_dttm customers_load_dttm, dp.load_dttm products_load_dttm
                        FROM
                            dwh.f_order fo
                            INNER JOIN dwh.d_craftsman dc ON fo.craftsman_id = dc.craftsman_id
                            INNER JOIN dwh.d_customer dcs ON fo.customer_id = dcs.customer_id
                            INNER JOIN dwh.d_product dp ON fo.product_id = dp.product_id
                            INNER JOIN dwh_update_delta ud ON fo.customer_id = ud.customer_id
                    ) customers
                GROUP BY
                    customers.customer_id,
                    customers.customer_name,
                    customers.customer_address,
                    customers.customer_birthday,
                    customers.customer_email,
                    customers.report_period
            ) aggr
            INNER JOIN (
                SELECT
                    dd.customer_id customer_id,
                    dd.craftsman_id top_craftsman_id,
                    count(dd.order_id) count_order,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            dd.customer_id
                        ORDER BY count(dd.order_id), count(dd.order_id) DESC
                    ) rank_count
                FROM dwh_delta dd
                GROUP BY
                    dd.customer_id,
                    dd.craftsman_id
            ) top_craftsman ON aggr.customer_id = top_craftsman.customer_id
            AND top_craftsman.rank_count = 1
            INNER JOIN (
                SELECT
                    dd.customer_id customer_id,
                    dd.product_type,
                    count(product_id) count_product,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            dd.customer_id
                        ORDER BY dd.product_type, count(product_id) DESC
                    ) rank_count
                FROM dwh_delta dd
                GROUP BY
                    dd.customer_id,
                    dd.product_type
            ) AS top_product ON aggr.customer_id = top_product.customer_id
            AND top_product.rank_count = 1
    ),
    insert_delta AS (
        INSERT INTO
            dwh.customer_report_datamart (
                customer_id,
                customer_name,
                customer_address,
                customer_birthday,
                customer_email,
                customer_money,
                platform_money,
                count_order,
                avg_price_order,
                median_time_order_completed,
                top_product_category,
                top_craftsman_id,
                count_order_created,
                count_order_in_progress,
                count_order_delivery,
                count_order_done,
                count_order_not_done,
                report_period
            )
        SELECT
            ddir.customer_id,
            ddir.customer_name,
            ddir.customer_address,
            ddir.customer_birthday,
            ddir.customer_email,
            ddir.customer_money,
            ddir.platform_money,
            ddir.count_order,
            ddir.avg_price_order,
            ddir.median_time_order_completed,
            ddir.top_product_category,
            ddir.top_craftsman_id,
            ddir.count_order_created,
            ddir.count_order_in_progress,
            ddir.count_order_delivery,
            ddir.count_order_done,
            ddir.count_order_not_done,
            ddir.report_period
        FROM dwh_delta_insert_result ddir
    ),
    update_delta AS (
        UPDATE dwh.customer_report_datamart
        SET
            customer_name = ddur.customer_name,
            customer_address = ddur.customer_address,
            customer_birthday = ddur.customer_birthday,
            customer_email = ddur.customer_email,
            customer_money = ddur.customer_money,
            platform_money = ddur.platform_money,
            count_order = ddur.count_order,
            avg_price_order = ddur.avg_price_order,
            median_time_order_completed = ddur.median_time_order_completed,
            top_product_category = ddur.top_product_category,
            top_craftsman_id = ddur.top_craftsman_id,
            count_order_created = ddur.count_order_created,
            count_order_in_progress = ddur.count_order_in_progress,
            count_order_delivery = ddur.count_order_delivery,
            count_order_done = ddur.count_order_done,
            count_order_not_done = ddur.count_order_not_done,
            report_period = ddur.report_period
        FROM (
               SELECT
                    customer_id,
                    customer_name,
                    customer_address,
                    customer_birthday,
                    customer_email,
                    customer_money,
                    platform_money,
                    count_order,
                    avg_price_order,
                    median_time_order_completed,
                    top_product_category,
                    top_craftsman_id,
                    count_order_created,
                    count_order_in_progress,
                    count_order_delivery,
                    count_order_done,
                    count_order_not_done,
                    report_period 
                FROM dwh_delta_update_result 
            ) ddur
        WHERE ddur.customer_id = dwh.customer_report_datamart.customer_id
    ),
    insert_load_date AS ( -- делаем запись в таблицу загрузок о том, когда была совершена загрузка, чтобы в следующий раз взять данные, которые будут добавлены или изменены после этой даты
    INSERT INTO dwh.load_dates_customer_report_datamart (
        load_dttm
    )
    SELECT GREATEST(COALESCE(MAX(craftsman_load_dttm), NOW()), 
                    COALESCE(MAX(customers_load_dttm), NOW()), 
                    COALESCE(MAX(products_load_dttm), NOW())) 
        FROM dwh_delta
)
SELECT 'increment datamart';