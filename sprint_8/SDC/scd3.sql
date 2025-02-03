DROP TABLE IF EXISTS public.table_scd3;

CREATE TABLE IF NOT EXISTS public.table_scd3 (
    id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    inn INT NOT NULL,
    company_name TEXT NOT NULL,
    previous_company_name TEXT NULL DEFAULT NULL,
    update_date DATE NOT NULL,
    CONSTRAINT table_scd3_pk PRIMARY KEY (id)
);