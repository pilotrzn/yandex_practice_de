BEGIN;
LOCK TABLE tasty.orders ;

update tasty.orders 
SET delivery_price = 500
WHERE o.amount < 1000;

COMMIT;

