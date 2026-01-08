WITH avg_rate AS (
SELECT 
	dd.courier_id ,
	fd.order_id ,
	avg(fd.rate) over(PARTITION BY dd.courier_id) avg_rate
FROM dds.fct_deliveries fd
INNER JOIN dds.dm_deliveries dd ON dd.id = fd.delivery_id 
), couriers_sum AS (
SELECT 
	dc.id courier_id,
	dc.courier_name,
	dt."year" settlement_year,
	dt."month" AS settlement_month,
	ar.avg_rate,
	count(DISTINCT do2.id) order_count,
	sum(fd.sum) total_sum,
	sum(fd.sum) * 0.25 order_processing_fee,
    SUM(fd.tip_sum) courier_tips_sum,
    sum(CASE			    
        WHEN ar.avg_rate < 4 THEN greatest(fd.sum * 0.05, 100)
        WHEN ar.avg_rate >= 4 AND ar.avg_rate < 4.5 THEN greatest(fd.sum * 0.07, 150)
        WHEN ar.avg_rate >= 4.5 AND ar.avg_rate < 4.9 THEN greatest(fd.sum * 0.07, 175)
        WHEN ar.avg_rate >= 4.9 THEN greatest (fd.sum * 0.1, 200)
    END) AS courier_order_sum
FROM dds.fct_deliveries fd 
INNER JOIN avg_rate ar ON fd.order_id = ar.order_id
INNER JOIN dds.dm_orders do2 ON do2.id = fd.order_id 
INNER JOIN dds.dm_timestamps dt ON dt.id = do2.timestamp_id 
INNER JOIN dds.dm_deliveries dd ON dd.id = fd.delivery_id 
INNER JOIN dds.dm_couriers dc ON dc.id = dd.courier_id 
WHERE do2.order_status = 'CLOSED'
AND dt."year" = EXTRACT('year' from current_date) 
AND dt."month" = EXTRACT('month' from current_date) - 1
GROUP BY 1,2,3,4,5)
SELECT 
	cs.courier_id,
	cs.courier_name,
	cs.settlement_year,
	cs.settlement_month,
	cs.avg_rate,
	cs.order_count,
	cs.total_sum,
	cs.order_processing_fee,
	cs.courier_tips_sum,
	cs.courier_order_sum,
	cs.courier_order_sum + cs.courier_tips_sum * 0.95 courier_reward_sum
FROM couriers_sum cs;