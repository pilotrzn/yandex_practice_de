/*Создание таблицы nf_lesson.craftsman_craftsman_status_6nf*/

DROP TABLE IF EXISTS nf_lesson.craftsman_craftsman_status_6nf;
CREATE TABLE nf_lesson.craftsman_craftsman_status_6nf AS
SELECT DISTINCT craftsman, craftsman_status, create_dttm
FROM nf_lesson.marketplace_craftsman_5nf; 

/*Создание таблицы nf_lesson.marketplace_craftsman_6nf*/

DROP TABLE IF EXISTS nf_lesson.marketplace_craftsman_6nf;
CREATE TABLE nf_lesson.marketplace_craftsman_6nf AS
SELECT DISTINCT marketplace, craftsman, create_dttm    
FROM nf_lesson.marketplace_craftsman_5nf; 

/*Создание таблицы nf_lesson.craftsman_product_6nf*/

DROP TABLE IF EXISTS nf_lesson.craftsman_product_6nf;
CREATE TABLE nf_lesson.craftsman_product_6nf AS
SELECT DISTINCT craftsman, product, create_dttm    
FROM nf_lesson.craftsman_product_5nf; 

