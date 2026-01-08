INSERT INTO stg.deliverysystem_deliveries
(delivery_id, delivery_value)
VALUES (%(delivery_id)s, %(delivery_value)s)
ON CONFLICT (delivery_id) DO UPDATE
SET delivery_value = EXCLUDED.delivery_value;