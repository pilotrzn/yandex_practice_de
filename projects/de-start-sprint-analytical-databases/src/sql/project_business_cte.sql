WITH limit_groups AS (
  SELECT hg.hk_group_id 
    FROM STV202504297__DWH.h_groups hg
ORDER BY hg.registration_dt 
   LIMIT 10)
,user_group_messages AS (
    SELECT lgd.hk_group_id hk_group_id, 
	       COUNT(DISTINCT lum.hk_user_id) cnt_users_in_group_with_messages
      FROM STV202504297__DWH.l_groups_dialogs lgd 
INNER JOIN STV202504297__DWH.l_user_message lum 
        ON lgd.hk_message_id = lum.hk_message_id 
INNER JOIN limit_groups lg 
        ON lg.hk_group_id = lgd.hk_group_id
  GROUP BY lgd.hk_group_id
    HAVING COUNT(DISTINCT lum.hk_user_id) >= 1)
,user_group_log AS (
    SELECT luga.hk_group_id hk_group_id, 
	       count(DISTINCT luga.hk_user_id) cnt_added_users
      FROM STV202504297__DWH.l_user_group_activity luga 
INNER JOIN limit_groups lg 
        ON lg.hk_group_id = luga.hk_group_id
INNER JOIN STV202504297__DWH.s_auth_history sah 
        ON sah.hk_l_user_group_activity = luga.hk_l_user_group_activity 
       AND sah.event = 'add'
  GROUP BY luga.hk_group_id
    HAVING count(DISTINCT luga.hk_user_id) > 1
    )
    SELECT ugl.hk_group_id,
	       ugl.cnt_added_users,
	       ugm.cnt_users_in_group_with_messages,
	       round(100 * ugm.cnt_users_in_group_with_messages / ugl.cnt_added_users, 2) group_conversion
      FROM user_group_log ugl
INNER JOIN user_group_messages ugm ON ugl.hk_group_id = ugm.hk_group_id
  ORDER BY 4 DESC;