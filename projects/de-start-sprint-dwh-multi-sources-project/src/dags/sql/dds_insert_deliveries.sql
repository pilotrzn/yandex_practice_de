INSERT INTO dds.dm_deliveries
(delivery_id, courier_id, delivery_ts_id, address)
VALUES (%(delivery_id)s, %(courier_id)s, %(delivery_ts_id)s, %(address)s)
ON CONFLICT (delivery_id) DO UPDATE
SET 
    courier_id = EXCLUDED.courier_id,
    delivery_ts_id = EXCLUDED.delivery_ts_id,
    address = EXCLUDED.address; 