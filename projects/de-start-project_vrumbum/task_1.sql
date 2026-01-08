SELECT 
    round(CAST(100 * (count(*) - count(m.gasoline_consumption))::real/count(*) AS NUMERIC), 2) nulls_percentage_gasoline_consumption
FROM car_auto.models m;
