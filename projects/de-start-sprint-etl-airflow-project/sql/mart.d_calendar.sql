    WITH all_dates as(
    SELECT  distinct date_id dt
    FROM    stage.customer_research cr
    UNION
    SELECT  DISTINCT date_time dt
    FROM    stage.user_activity_log ual
    UNION
    SELECT  DISTINCT date_time dt
    FROM    stage.user_order_log uol
    )
    INSERT INTO mart.d_calendar
    (fact_date, day_num, week_num, month_num, month_name, year_num)
    SELECT
        ad.dt,
        EXTRACT (DAY FROM ad.dt),
        EXTRACT(WEEK FROM ad.dt),
        EXTRACT(MONTH FROM ad.dt),
        trim(to_char(ad.dt, 'Mon')),
        EXTRACT(YEAR FROM ad.dt)
    FROM
        all_dates ad
    where ad.dt::date NOT in(SELECT fact_date FROM mart.d_calendar)
    ORDER BY ad.dt;