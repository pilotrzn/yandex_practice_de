INSERT INTO dds.fct_deliveries
(delivery_id, order_id, sum, tip_sum, rate)
VALUES (%(delivery_id)s, %(order_id)s, %(sum)s, %(tip_sum)s, %(rate)s)
ON CONFLICT (delivery_id, order_id) DO UPDATE
SET 
    sum = EXCLUDED.sum,
    tip_sum = EXCLUDED.tip_sum,
    rate = EXCLUDED.rate;