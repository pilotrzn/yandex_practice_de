WITH deliveries AS (
SELECT 
	id,
	delivery_id,
	delivery_value::json->>'courier_id' courier_id,
	delivery_value::json->>'address' address,
	(delivery_value::json->>'delivery_ts')::timestamp delivery_ts,
	delivery_value::json->>'rate' rate,
	delivery_value::json->>'tip_sum' tip_sum
FROM stg.deliverysystem_deliveries)
SELECT 
	dl.id,
	dl.delivery_id,
	dc.id courier_id,
	ddt.id delivery_ts_id,
	dl.address
FROM deliveries dl
INNER JOIN dds.dm_couriers dc ON dc.courier_id = dl.courier_id
INNER JOIN dds.dm_delivery_timestamps ddt ON ddt.ts = dl.delivery_ts
WHERE dl.id > %(threshold)s 
ORDER BY dl.id ASC
LIMIT %(limit)s;