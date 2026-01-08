--stg
DROP TABLE IF EXISTS STV202504297__STAGING.group_log;
DROP TABLE IF EXISTS STV202504297__STAGING.group_log_rejected;

CREATE TABLE  STV202504297__STAGING.group_log(
	group_id int NOT NULL,
	user_id int NOT NULL,
	user_id_from int NULL,
	event varchar(10) NOT NULL,
	datetime timestamp(0)
	)
	ORDER BY datetime
	PARTITION BY datetime::date
	GROUP BY calendar_hierarchy_day(datetime::date, 3, 2);
--################

--link
DROP TABLE IF EXISTS STV202504297__DWH.l_user_group_activity;

CREATE TABLE STV202504297__DWH.l_user_group_activity
(
    hk_l_user_group_activity bigint PRIMARY KEY,
    hk_user_id bigint NOT NULL CONSTRAINT fk_l_groups_dialogs_dialog references STV202504297__DWH.h_users (hk_user_id),
    hk_group_id bigint NOT NULL CONSTRAINT fk_l_lgroups_dialogs_group references STV202504297__DWH.h_groups (hk_group_id),
    load_dt timestamp,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_l_user_group_activity all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2); 
--##################

--satellite
DROP TABLE STV202504297__DWH.s_auth_history;

CREATE TABLE STV202504297__DWH.s_auth_history(
    hk_l_user_group_activity bigint NOT NULL CONSTRAINT fk_s_auth_history_l_user_group_activity REFERENCES l_user_group_activity(hk_l_user_group_activity),
    user_id_from bigint NULL,
    event varchar(10),
    event_dt timestamp, 
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_l_user_group_activity all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);