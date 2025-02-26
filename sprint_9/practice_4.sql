EXPLAIN
SELECT * 
FROM my_table 
INNER JOIN (
	VALUES ('22022-03-141'),('22022-03-142'),('22022-03-143'),('22022-03-144'),('22022-03-145'),
           ('22022-03-146'),('22022-03-147'),('22022-03-148'),('22022-03-149'),('22022-03-1410')
           ) AS v(property_two)
USING(property_two);


EXPLAIN
SELECT *
FROM my_table mt, my_table_dump mtd
WHERE 
mt.id < 11 AND mt.id > 0 AND mtd.id > 5 AND mtd.id < 11
limit 50;