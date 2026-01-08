INSERT INTO dds.dm_delivery_timestamps
(ts, "year", "month", "day", "time", "date")
VALUES (%(ts)s, %(year)s, %(month)s, %(day)s, %(time)s, %(date)s)
ON CONFLICT (ts) DO UPDATE
SET
    year = EXCLUDED.year,
    month = EXCLUDED.month,
    day = EXCLUDED.day,
    time = EXCLUDED.time,
    date = EXCLUDED.date;