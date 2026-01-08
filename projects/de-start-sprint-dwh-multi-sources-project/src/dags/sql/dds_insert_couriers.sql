INSERT INTO dds.dm_couriers
(courier_id, courier_name)
VALUES (%(courier_id)s, %(courier_name)s)
ON CONFLICT (courier_id) DO UPDATE
SET
    courier_name = EXCLUDED.courier_name;