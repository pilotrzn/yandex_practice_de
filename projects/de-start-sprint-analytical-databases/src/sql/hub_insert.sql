INSERT INTO STV202504297__DWH.h_users(
hk_user_id, user_id,registration_dt,load_dt,load_src)
SELECT
	hash(u1.id) as hk_user_id,
	u1.id as user_id,
	u1.registration_dt,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.users u1
WHERE NOT EXISTS 
(SELECT 1 FROM STV202504297__DWH.h_users u2
	WHERE hash(u1.id) = u2.hk_user_id)
ORDER BY u1.id;
	
INSERT INTO STV202504297__DWH.h_groups
(hk_group_id, group_id, registration_dt, load_dt, load_src)
SELECT
	hash(g1.id) as hk_group_id,
	g1.id as group_id,
	g1.registration_dt,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.groups g1
WHERE NOT EXISTS 
(SELECT 1 FROM STV202504297__DWH.h_groups g2
	WHERE hash(g1.id) = g2.hk_group_id);
	
INSERT INTO STV202504297__DWH.h_dialogs
(hk_message_id, message_id, message_ts, load_dt, load_src)
SELECT
	hash(d1.message_id) as hk_message_id,
	d1.message_id as message_id,
	d1.message_ts ,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.dialogs d1
WHERE NOT EXISTS 
(SELECT 1 FROM STV202504297__DWH.h_dialogs d2
	WHERE hash(d1.message_id) = d2.hk_message_id)
ORDER BY d1.message_id ;

