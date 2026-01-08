INSERT INTO stg.deliverysystem_restaurants
(restaurant_id, "name")
VALUES (%(restaurant_id)s, %(name)s)
ON CONFLICT (restaurant_id) DO UPDATE
SET
    name = EXCLUDED.name;