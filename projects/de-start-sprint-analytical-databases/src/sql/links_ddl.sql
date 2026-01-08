drop table if exists STV202504297__DWH.l_admins;
drop table if exists STV202504297__DWH.l_user_message;
drop table if exists STV202504297__DWH.l_groups_dialogs;

CREATE TABLE STV202504297__DWH.l_admins
(
    hk_l_admin_id int NOT NULL primary key,
    hk_user_id int NOT NULL CONSTRAINT fk_l_admins_user references STV202504297__DWH.h_users (hk_user_id),
    hk_group_id int NOT NULL CONSTRAINT fk_l_admins_group references STV202504297__DWH.h_groups (hk_group_id),
    load_dt timestamp,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_l_admin_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2); 


CREATE TABLE STV202504297__DWH.l_user_message
(
    hk_l_user_message bigint primary key,
    hk_user_id bigint NOT NULL CONSTRAINT fk_l_user_message_user references STV202504297__DWH.h_users (hk_user_id),
    hk_message_id bigint NOT NULL CONSTRAINT fk_l_user_message_message references STV202504297__DWH.h_dialogs (hk_message_id),
    load_dt timestamp,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_user_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2); 

CREATE TABLE STV202504297__DWH.l_groups_dialogs
(
    hk_l_groups_dialogs bigint PRIMARY KEY,
    hk_message_id bigint NOT NULL CONSTRAINT fk_l_groups_dialogs_dialog references STV202504297__DWH.h_dialogs (hk_message_id),
    hk_group_id bigint NULL CONSTRAINT fk_l_lgroups_dialogs_group references STV202504297__DWH.h_groups (hk_group_id),
    load_dt timestamp,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_l_groups_dialogs all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2); 

