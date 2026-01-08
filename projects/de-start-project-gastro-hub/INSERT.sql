/*Добавьте в этот файл запросы, которые наполняют данными таблицы в схеме cafe данными*/

INSERT INTO cafe.restaurants (restaurant_name, restaurant_type)
SELECT DISTINCT cafe_name ,s."type"::cafe.restaurant_type  
FROM gastrohub.raw_data.sales s 
RETURNING *;

UPDATE cafe.restaurants 
SET restaurant_menu = m.menu 
FROM raw_data.menu m 
where cafe.restaurants.restaurant_name = m.cafe_name 
RETURNING *;

INSERT INTO cafe.managers (manager_name, manager_phone)
SELECT DISTINCT s.manager ,s.manager_phone 
FROM raw_data.sales s 
RETURNING *;

INSERT INTO cafe.restaurant_manager_work_dates(begin_work_date,end_work_date,manager_uuid,restaurant_uuid)
SELECT min(s.report_date), max(s.report_date), m.manager_uuid ,r.restaurant_uuid 
FROM raw_data.sales s 
LEFT JOIN cafe.managers m ON m.manager_name = s.manager 
LEFT JOIN cafe.restaurants r ON r.restaurant_name = s.cafe_name 
GROUP BY m.manager_uuid ,r.restaurant_uuid
RETURNING *;

INSERT INTO cafe.sales(sale_date,restaurant_uuid ,avg_check)
SELECT s.report_date ,r.restaurant_uuid ,s.avg_check 
FROM raw_data.sales s 
LEFT JOIN cafe.restaurants r ON r.restaurant_name = s.cafe_name 
RETURNING *;