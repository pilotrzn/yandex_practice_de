DROP TABLE if exists public.passport;

CREATE TABLE IF NOT EXISTS public.passport (
id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
series INT NOT NULL,
number INT NOT NULL,
birthday DATE NOT NULL,
birthplace TEXT NOT NULL,
CONSTRAINT passport_pk PRIMARY key(id)
);


REVOKE UPDATE ON public.passport FROM de_sp1_20250130_6640bf9a18;