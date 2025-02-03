INSERT INTO public.table_scd6(code,"name",actual_status, historical_status,start_date)
VALUES ('A1B2', 'Jhon', 'A2', 'A2', '2023-01-01');

UPDATE public.table_scd6 
SET historical_status = 'A1',
	actual_status = 'A2',
	end_date = '2023-01-02'
WHERE code = 'A1B2' AND actual_status ='A1';