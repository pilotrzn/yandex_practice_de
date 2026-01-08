INSERT INTO STV202504297__DWH.l_user_group_activity
(hk_l_user_group_activity, hk_user_id, hk_group_id, load_dt, load_src)
SELECT DISTINCT 
	hash(hu.hk_user_id, hg.hk_group_id),
	hu.hk_user_id,
	hg.hk_group_id,
	now() AS load_dt,
	's3' AS load_src
FROM STV202504297__STAGING.group_log gl 
LEFT JOIN STV202504297__DWH.h_users hu ON hu.user_id = gl.user_id 
LEFT JOIN STV202504297__DWH.h_groups hg ON hg.group_id = gl.group_id
WHERE hu.user_id IS NOT null;


INSERT INTO STV202504297__DWH.s_auth_history
(hk_l_user_group_activity, user_id_from, event, event_dt, load_dt, load_src)
SELECT 
	hash(hu.hk_user_id, hg.hk_group_id),
	gl.user_id_from ,
	gl.event ,
	gl.datetime,
	now() AS load_dt,
	's3' AS load_src
from STV202504297__STAGING.group_log as gl
left join STV202504297__DWH.h_groups as hg on gl.group_id = hg.group_id
left join STV202504297__DWH.h_users as hu on gl.user_id = hu.user_id
left join STV202504297__DWH.l_user_group_activity as luga on hg.hk_group_id = luga.hk_group_id and hu.hk_user_id = luga.hk_user_id;