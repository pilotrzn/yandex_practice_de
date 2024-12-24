BEGIN TRANSACTION ISOLATION LEVEL repeatable read;
UPDATE users
SET balance = balance + new_balance.summ
FROM 
(SELECT user_id ,sum(amount) summ 
FROM operations o  
GROUP BY user_id) new_balance 
WHERE new_balance.user_id = id;

commit;


BEGIN;
    SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
    UPDATE users u
    SET balance = balance + new_balance + (10 * (balance + new_balance)/100)
    FROM (
        SELECT user_id, SUM(amount) as new_balance
        FROM operations
        GROUP BY user_id
    ) o
    WHERE u.id = o.user_id;
COMMIT;