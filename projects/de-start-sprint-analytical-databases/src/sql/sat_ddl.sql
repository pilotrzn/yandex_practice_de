drop table if exists STV202504297__DWH.s_admins;
drop table if exists STV202504297__DWH.s_user_socdem;
drop table if exists STV202504297__DWH.s_user_chat_info;
drop table if exists STV202504297__DWH.s_group_name;
drop table if exists STV202504297__DWH.s_group_private_status;
drop table if exists STV202504297__DWH.s_dialog_info;

create table STV202504297__DWH.s_admins
(
hk_admin_id bigint NOT NULL CONSTRAINT fk_s_admins_l_admins REFERENCES STV202504297__DWH.l_admins (hk_l_admin_id),
is_admin boolean,
admin_from datetime,
load_dt datetime,
load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_admin_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);


CREATE TABLE STV202504297__DWH.s_user_socdem(
    hk_user_id bigint not null constraint fk_s_user_socdem_h_user REFERENCES STV202504297__DWH.h_users(hk_user_id),
    chat_name varchar(200),
    country varchar(200),
    age int,
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_user_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

CREATE TABLE STV202504297__DWH.s_user_chat_info(
    hk_user_id bigint not null constraint s_user_chat_info_h_user REFERENCES STV202504297__DWH.h_users(hk_user_id),
    chat_name varchar(200),
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_user_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

CREATE TABLE STV202504297__DWH.s_group_name(
    hk_group_id bigint not null CONSTRAINT fk_s_group_name_h_groups REFERENCES STV202504297__DWH.h_groups(hk_group_id),
    group_name varchar(100),
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_group_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

CREATE TABLE STV202504297__DWH.s_group_private_status(
    hk_group_id bigint not null CONSTRAINT fk_s_group_private_status_h_groups REFERENCES STV202504297__DWH.h_groups(hk_group_id),
    is_private boolean,
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_group_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

CREATE TABLE STV202504297__DWH.s_dialog_info(
    hk_message_id bigint not null CONSTRAINT fk_s_gialog_info_h_dialogs REFERENCES STV202504297__DWH.h_dialogs(hk_message_id),
    message varchar(1000),
    message_from int,
    message_to int, 
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_message_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);