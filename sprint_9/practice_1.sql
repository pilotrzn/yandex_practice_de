DROP TABLE IF EXISTS public.application_users_dm;

CREATE TABLE IF NOT EXISTS public.application_users_dm (
    id bigint GENERATED ALWAYS AS IDENTITY,
    login varchar(32) not null,
    fullname text not null,
    age smallint check(age > 14) not null,
    created_date date not null,
    last_visit_date timestamptz not null,
    subscription bool not null default False ,
    avg_time_in_app_hh numeric(10,1) check(avg_time_in_app_hh >= 0) not null default 0,
    day_max_time_in_the_app smallint check(day_max_time_in_the_app > 0 and day_max_time_in_the_app < 8) not null,
    activity_percentage numeric(10,1) check (activity_percentage >=0 ) not null,
    constraint application_users_dm_pk primary key(id)
);

WITH 
hr AS (
SELECT employee_id, salary, department 
FROM hr_data 
WHERE work_experience < 5
), 
personal AS (
SELECT employee_id 
FROM personal_data pd 
WHERE  pd.age < 35
)
SELECT  avg(h.salary), h.department
FROM hr h 
INNER JOIN personal p using(employee_id)
GROUP BY h.department;