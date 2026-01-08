WITH dts AS (
	SELECT 
		id,
		(delivery_value::json->>'delivery_ts')::timestamp ts
	FROM stg.deliverysystem_deliveries)
SELECT 
	dts.id,
	dts.ts,
	EXTRACT (YEAR FROM dts.ts) "year",
	EXTRACT (MONTH FROM dts.ts) "month",
	EXTRACT (DAY FROM dts.ts) "day",
	dts.ts::date "date",
	dts.ts::time "time"
FROM dts
WHERE dts.id > %(threshold)s 
ORDER BY dts.id ASC
LIMIT %(limit)s;