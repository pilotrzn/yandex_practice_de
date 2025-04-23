DROP TABLE IF EXISTS nf_lesson.marketplace_craftsman_5nf;
CREATE TABLE nf_lesson.marketplace_craftsman_5nf AS
SELECT DISTINCT marketplace, craftsman 
FROM nf_lesson.source_5nf;

DROP TABLE IF EXISTS nf_lesson.marketplace_product_5nf;
CREATE TABLE nf_lesson.marketplace_product_5nf AS
SELECT DISTINCT marketplace, product
FROM nf_lesson.source_5nf;

DROP TABLE IF EXISTS nf_lesson.craftsman_product_5nf;
CREATE TABLE nf_lesson.craftsman_product_5nf AS
SELECT craftsman, product, craftsman_status , create_dttm
FROM nf_lesson.source_5nf;

SELECT mp.marketplace, cp.craftsman, cp.product, mp.create_dttm ,mc.craftsman_status 
FROM  nf_lesson.marketplace_craftsman_5nf mc 
JOIN nf_lesson.marketplace_product_5nf mp ON mp.marketplace = mc.marketplace 
JOIN nf_lesson.craftsman_product_5nf cp ON cp.craftsman = mc.craftsman 
AND cp.product = mp.product 
limit 11;