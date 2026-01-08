WITH dlvrs AS (
SELECT 
	dd.id,
	dd.delivery_id,
	dd.delivery_value::json->>'order_id' order_id,
	(dd.delivery_value::json->>'sum')::numeric(14,2) sum,
	(dd.delivery_value::json->>'tip_sum')::numeric(14,2) tip_sum, 
	(dd.delivery_value::json->>'rate')::int rate 
FROM stg.deliverysystem_deliveries dd)
SELECT 
	dlvr.id,
	ddd.id delivery_id,
	do2.id order_id,
	dlvr.sum sum,
	dlvr.tip_sum tip_sum,
	dlvr.rate rate
FROM dlvrs dlvr
INNER JOIN dds.dm_orders do2 ON do2.order_key = dlvr.order_id
INNER JOIN dds.dm_deliveries ddd ON ddd.delivery_id = dlvr.delivery_id
WHERE dlvr.id > %(threshold)s 
ORDER BY dlvr.id ASC
LIMIT %(limit)s;