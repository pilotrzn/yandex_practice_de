SELECT 
	id,
	object_id courier_id,
	object_value::json->>'name' courier_name
FROM stg.deliverysystem_couriers
WHERE id > %(threshold)s
ORDER BY id
LIMIT %(limit)s;