SELECT id, parent_id, product_name
FROM students.products;

WITH RECURSIVE prod AS (
    SELECT 
        id, 
        parent_id, 
        1 lvl,
        product_name
    FROM students.products 
    WHERE product_name = 'Имущество ФЛ'
    UNION 
    SELECT distinct
        main.id, 
        main.parent_id, 
        lvl + 1,
        main.product_name
    FROM students.products main
    JOIN prod rec_prod ON main.parent_id = rec_prod.id     
)
SELECT id, parent_id, product_name
FROM prod
WHERE parent_id = 5 


WITH RECURSIVE prod AS (
    SELECT 
        id, 
        parent_id, 
        1 lvl,
        product_name,
        product_name::TEXT full_path
    FROM students.products 
    WHERE product_name = 'Авто'
    UNION 
    SELECT distinct
        main.id, 
        main.parent_id, 
        lvl + 1,
        main.product_name,
        concat(rec_prod.full_path, '-',main.product_name) full_path
    FROM students.products main
    JOIN prod rec_prod ON main.parent_id = rec_prod.id     
)
SELECT id, parent_id, lvl, product_name, full_path
FROM prod
ORDER BY full_path 


WITH RECURSIVE product_path AS (
    SELECT 
        id, 
        parent_id, 
        1 lvl,
        product_name,
        product_name::TEXT full_path
    FROM students.products 
    WHERE product_name = '2. Зелёная карта ФЛ, 131'
    UNION 
    SELECT distinct
        main.id, 
        main.parent_id, 
        lvl + 1,
        rec_prod.product_name,
        concat(rec_prod.full_path, '/',main.product_name) full_path
    FROM students.products main
    INNER JOIN product_path rec_prod ON main.id = rec_prod.parent_id     
)
SELECT full_path
FROM product_path
WHERE parent_id IS NULL;

