# Проект Врум-Бум!. Сырые данные


Все команды выполнялись с личного сервера, на котором установлен postgresql. Работы выполнялись под локальным пользователем postgres.
Для подключения создан файл .pgpass

## Скачивание файла

```bash
$ sudo -iu postgres
$ psql -h rc1a-098ppz48slkroxr7.mdb.yandexcloud.net -p 6432 -U de_start_20241114_8186acad5b playground_start_20241114_8186acad5b
```

скачиваем файл с данными

```bash
$ mkdir ya_proj
$ cd ya_proj
$ wget https://code.s3.yandex.net/Data_engeneer/datasets/cars.csv?etag=502fd866b0bb7a77592508164da16ce8 -O cars.csv
$ ls -l 
-rw-r--r-- 1 postgres postgres 90936 Aug 16 23:14 cars.csv
```

## Создание БД 

```sql
playground_start_20241114_8186acad5b=> create schema raw_data;
playground_start_20241114_8186acad5b=> 
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
playground_start_20241114_8186acad5b=> \copy raw_data.sales(id,auto,gasoline_consumption,price,date,person_name,phone,discount,brand_origin) FROM /var/lib/pgsql/ya_proj/cars.csv CSV HEADER NULL 'null';
COPY 1000
```
