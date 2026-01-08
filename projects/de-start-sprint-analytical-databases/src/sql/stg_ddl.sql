DROP TABLE IF EXISTS STV202504297__STAGING.users;
DROP TABLE IF EXISTS STV202504297__STAGING.groups;
DROP TABLE IF EXISTS STV202504297__STAGING.dialogs;
DROP TABLE IF EXISTS STV202504297__STAGING.users_rejected;
DROP TABLE IF EXISTS STV202504297__STAGING.groups_rejected;
DROP TABLE IF EXISTS STV202504297__STAGING.dialogs_rejected;


CREATE TABLE STV202504297__STAGING.users(
	id int PRIMARY KEY,
	chat_name varchar(200),
	registration_dt timestamp(0),
	country varchar(200),
	age int)
	ORDER BY id;

CREATE TABLE  STV202504297__STAGING.groups(
	id int PRIMARY key,
	admin_id int,
	group_name varchar(100),
	registration_dt timestamp(0),
	is_private boolean
	)
	ORDER BY id, admin_id
	PARTITION BY registration_dt::date
	GROUP BY calendar_hierarchy_day(registration_dt::date, 3, 2);

CREATE TABLE STV202504297__STAGING.dialogs(
	message_id int PRIMARY KEY,
	message_ts timestamp(6),
	message_from int,
	message_to int,
	message varchar(1000),
	message_group int
	)
	ORDER BY message_id
	PARTITION BY message_ts::date
	GROUP BY calendar_hierarchy_day(message_ts::date, 3, 2);
	

