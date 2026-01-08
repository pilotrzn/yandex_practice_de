create schema raw_data;
create table raw_data.sales(
    id integer,
    auto text,
    gasoline_consumption numeric(3,1),
    price numeric(9,2) ,
    date timestamp DEFAULT CURRENT_TIMESTAMP ,
    person_name text,
    phone text null,
    discount numeric(5,2) ,
    brand_origin text 
);
\copy raw_data.sales(id,auto,gasoline_consumption,price,date,person_name,phone,discount,brand_origin) FROM /var/lib/pgsql/ya_proj/cars.csv CSV HEADER NULL 'null';

--в результате загружено 1000 записей
