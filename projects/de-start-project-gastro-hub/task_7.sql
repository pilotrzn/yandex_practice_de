-- Руководство GastroHub приняло решение сделать единый номер телефонов для всех менеджеров. 
-- Новый номер — 8-800-2500-***, где порядковый номер менеджера выставляется по алфавиту, начиная с номера 100. 
-- Старый и новый номер нужно будет хранить в массиве, где первый элемент массива — новый номер, а второй — старый.
-- Во время проведения этих изменений таблица managers должна быть недоступна для изменений со стороны других пользователей, но доступна для чтения.

BEGIN;

LOCK TABLE cafe.managers IN ACCESS EXCLUSIVE MODE;

ALTER TABLE cafe.managers ADD COLUMN manager_phones varchar[];

WITH managers_order AS (
SELECT 
	row_number() OVER (ORDER BY m.manager_name) rn,
	m.manager_uuid,
	m.manager_phone
FROM cafe.managers m)
,phone_arr as(
	SELECT 
		ARRAY[concat('8-800-2500-',100 + rn) ,manager_phone] phone_arr,
		manager_uuid
	FROM managers_order
)
UPDATE cafe.managers m
SET manager_phones = pa.phone_arr
FROM phone_arr  pa
WHERE m.manager_uuid = pa.manager_uuid
RETURNING  m.*;

ALTER TABLE cafe.managers DROP COLUMN manager_phone;

COMMIT;