SELECT 
	title,
	rental_rate,
	length,
	rating 
FROM chinook.movie m
WHERE rental_rate > 2
ORDER BY length desc
LIMIT 40;