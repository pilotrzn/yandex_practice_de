INSERT INTO STV202504297__DWH.l_admins(
	hk_l_admin_id, hk_group_id, hk_user_id, load_dt, load_src)
SELECT
hash(hg.hk_group_id,hu.hk_user_id),
hg.hk_group_id,
hu.hk_user_id,
now() AS load_dt,
's3' AS load_src
FROM STV202504297__STAGING.groups as g
LEFT JOIN h_users AS hu ON g.admin_id = hu.user_id
LEFT JOIN h_groups AS hg ON g.id = hg.group_id
WHERE NOT EXISTS (
	SELECT 1 FROM l_admins la 
	WHERE la.hk_l_admin_id = hash(hg.hk_group_id,hu.hk_user_id)
);

INSERT INTO STV202504297__DWH.l_user_message
(hk_l_user_message, hk_user_id, hk_message_id, load_dt, load_src)
SELECT DISTINCT 
	hash(hd.hk_message_id ,hu.hk_user_id),
	hd.hk_message_id,
	hu.hk_user_id, 
	now() AS load_dt,
	's3' AS load_src
FROM STV202504297__STAGING.dialogs d 
INNER JOIN h_dialogs hd ON hd.message_id = d.message_id 
INNER JOIN h_users hu ON d.message_from = hu.user_id 
WHERE NOT EXISTS (
	SELECT 1 FROM l_user_message lum 
	WHERE lum.hk_l_user_message = hash(hd.hk_message_id ,hu.hk_user_id)
);

INSERT INTO STV202504297__DWH.l_groups_dialogs
(hk_l_groups_dialogs, hk_message_id, hk_group_id, load_dt, load_src)
SELECT 
	hash(hg.hk_group_id, hd.hk_message_id),
	hd.hk_message_id ,
	hg.hk_group_id,
	now() AS load_dt,
	's3' AS load_src
FROM  STV202504297__STAGING.dialogs d
LEFT JOIN h_dialogs hd ON hd.message_id = d.message_id 
LEFT JOIN h_groups hg ON d.message_group = hg.group_id 
WHERE NOT EXISTS (
	SELECT 1 FROM l_groups_dialogs lgd 
	WHERE lgd.hk_l_groups_dialogs = hash(hg.hk_group_id, hd.hk_message_id)
);
