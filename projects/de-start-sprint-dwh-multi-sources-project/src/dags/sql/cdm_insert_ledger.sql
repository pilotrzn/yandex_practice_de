INSERT INTO cdm.dm_courier_ledger
(courier_id,
courier_name,
settlement_year,
settlement_month,
orders_count,
orders_total_sum,
rate_avg,
order_processing_fee,
courier_order_sum,
courier_tips_sum,
courier_reward_sum)
VALUES (%(courier_id)s, %(courier_name)s, %(settlement_year)s, %(settlement_month)s, %(orders_count)s, %(orders_total_sum)s,
%(rate_avg)s, %(order_processing_fee)s, %(courier_order_sum)s, %(courier_tips_sum)s, %(courier_reward_sum)s)
ON CONFLICT (courier_id, settlement_year, settlement_month) 
DO UPDATE
SET 
    courier_name = EXCLUDED.courier_name,
    orders_count = EXCLUDED.orders_count,
    orders_total_sum = EXCLUDED.orders_total_sum,
    rate_avg = EXCLUDED.rate_avg,
    order_processing_fee = EXCLUDED.order_processing_fee,
    courier_order_sum = EXCLUDED.courier_order_sum,
    courier_tips_sum = EXCLUDED.courier_tips_sum,
    courier_reward_sum = EXCLUDED.courier_reward_sum;