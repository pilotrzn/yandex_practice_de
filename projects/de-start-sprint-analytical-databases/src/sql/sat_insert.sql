INSERT INTO STV202504297__DWH.s_admins
	(hk_admin_id, is_admin, admin_from,load_dt,load_src)
SELECT
	la.hk_l_admin_id,
	True as is_admin,
	hg.registration_dt,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__DWH.l_admins as la
LEFT JOIN STV202504297__DWH.h_groups as hg on la.hk_group_id = hg.hk_group_id;

--s_user_socdem
INSERT INTO STV202504297__DWH.s_user_socdem
	(hk_user_id, country, age, load_dt, load_src)
SELECT 
	hu.hk_user_id ,
	u.country ,
	u.age ,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.users u 
LEFT JOIN STV202504297__DWH.h_users hu ON hu.user_id = u.id ;

--s_user_chatinfo
INSERT INTO STV202504297__DWH.s_user_chat_info
	(hk_user_id, chat_name, load_dt, load_src)
SELECT 
	hu.hk_user_id ,
	u.chat_name,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.users u 
LEFT JOIN STV202504297__DWH.h_users hu ON hu.user_id = u.id ;

INSERT INTO STV202504297__DWH.s_dialog_info
	(hk_message_id, message, message_from, message_to, load_dt, load_src)
SELECT 
	hd.hk_message_id ,
	d.message ,
	d.message_from ,
	d.message_to ,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.dialogs d 
LEFT JOIN STV202504297__DWH.h_dialogs hd ON hd.message_id = d.message_id ;


INSERT INTO STV202504297__DWH.s_group_name
	(hk_group_id, group_name, load_dt, load_src)
SELECT 
	hg.hk_group_id ,
	g.group_name ,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.groups g 
LEFT JOIN STV202504297__DWH.h_groups hg ON hg.group_id = g.id ;

INSERT INTO STV202504297__DWH.s_group_private_status
	(hk_group_id, is_private, load_dt, load_src)
SELECT 
	hg.hk_group_id ,
	g.is_private ,
	now() as load_dt,
	's3' as load_src
FROM STV202504297__STAGING.groups g 
LEFT JOIN STV202504297__DWH.h_groups hg ON hg.group_id = g.id ;