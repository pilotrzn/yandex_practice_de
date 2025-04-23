DROP TABLE IF EXISTS public.clients CASCADE ;
DROP TABLE IF EXISTS public.sales CASCADE ;
DROP TABLE IF EXISTS public.products CASCADE ;

CREATE TABLE public.clients
(
    client_id INTEGER NOT NULL
        CONSTRAINT clients_pk PRIMARY KEY,
    name      TEXT    NOT NULL,
    login     TEXT    NOT NULL
);
CREATE TABLE products
(
    product_id INTEGER        NOT NULL
        CONSTRAINT products_pk PRIMARY KEY,
    name       TEXT           NOT NULL,
    price      NUMERIC(14, 2) NOT NULL
);
CREATE TABLE sales
(
    client_id  INTEGER        NOT NULL
        CONSTRAINT sales_clients_client_id_fk REFERENCES clients,
    product_id INTEGER        NOT NULL
        CONSTRAINT sales_products_product_id_fk REFERENCES products,
    amount     INTEGER        NOT NULL,
    total_sum  NUMERIC(14, 2) NOT NULL,
    CONSTRAINT sales_pk PRIMARY KEY (client_id, product_id)
); 


ALTER TABLE public.sales DROP CONSTRAINT sales_products_product_id_fk;
ALTER TABLE public.products DROP CONSTRAINT products_pk;
ALTER TABLE public.products ADD COLUMN id INT NOT NULL;
ALTER TABLE public.products ALTER id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE public.products ADD CONSTRAINT product_pk PRIMARY key(id);
ALTER TABLE public.sales ADD CONSTRAINT sales_products_id_fk FOREIGN KEY (product_id) REFERENCES public.products(id);
ALTER TABLE public.products ADD COLUMN valid_from timestamptz ;
ALTER TABLE public.products  ADD COLUMN valid_to timestamptz;