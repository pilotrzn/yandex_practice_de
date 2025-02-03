DROP TABLE IF EXISTS dwh.f_order;
CREATE TABLE dwh.f_order (
    order_id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
  	product_id int8 NOT NULL,
    craftsman_id int8 NOT NULL,
  	customer_id int8 NOT NULL,
    order_created_date date NOT NULL,
    order_completion_date date NOT NULL,
    order_status VARCHAR NOT NULL CHECK (order_status IN ('created', 'in progress', 'delivery', 'done')),
    load_dttm timestamp NOT NULL,
    CONSTRAINT orders_pk PRIMARY KEY (order_id),
    CONSTRAINT orders_craftsman_fk FOREIGN KEY (craftsman_id) REFERENCES dwh.d_craftsman(craftsman_id) ON DELETE restrict,
    CONSTRAINT orders_customer_fk FOREIGN KEY (customer_id) REFERENCES dwh.d_customer(customer_id) ON DELETE restrict,
    CONSTRAINT orders_product_fk FOREIGN KEY (product_id) REFERENCES dwh.d_product(product_id) ON DELETE RESTRICT
); 
COMMENT ON TABLE dwh.f_order IS 'Таблица фактов';
COMMENT ON COLUMN dwh.f_order.order_id IS 'идентификатор заказа';
COMMENT ON COLUMN dwh.f_order.product_id IS 'идентификатор товара ручной работы';
COMMENT ON COLUMN dwh.f_order.craftsman_id IS 'идентификатор мастера';
COMMENT ON COLUMN dwh.f_order.customer_id IS 'идентификатор заказчика';
COMMENT ON COLUMN dwh.f_order.order_created_date IS ' дата создания заказа';
COMMENT ON COLUMN dwh.f_order.order_completion_date IS 'дата выполнения заказа';
COMMENT ON COLUMN dwh.f_order.order_status IS 'статус выполнения заказа';
COMMENT ON COLUMN dwh.f_order.load_dttm IS 'дата и время загрузки';


