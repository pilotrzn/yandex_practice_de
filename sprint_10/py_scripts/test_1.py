import psycopg2
import pandas as pd
import numpy as np
from psycopg2 import sql
from datetime import datetime


db_config = {
    'host': 'postgres',
    'port': '5432',
    'dbname': 'student',
    'user': 'student',
    'password': 'student-de',
    'options': '-c search_path=stage'
}

TABLE = 'table'
HEADERS = 'headers'
DATEFIELD = 'datefield'
TABLES = [
    {
        TABLE: 'customer_research',
        HEADERS: 'date_id,category_id,geo_id,sales_qty,sales_amt',
        DATEFIELD: 'date_id'
    },
    {
        TABLE: 'user_order_log',
        HEADERS: 'id,date_time,city_id,city_name,customer_id,first_name,last_name,item_id,item_name,quantity,payment_amount',
        DATEFIELD: 'date_time'
    },
    {
        TABLE: 'user_activity_log',
        HEADERS: 'id,date_time,action_id,customer_id,quantity',
        DATEFIELD: 'date_time'
    }
]
PATH_TO_FILES = '/lessons/2. Анализ вводных по задаче/7. Использование файлов и подключение к БД/Задание 1/stage'
CHUNK_SIZE = 100

conn = psycopg2.connect(**db_config)
cur = conn.cursor()

for current_table in TABLES:
    csv_file = f'{PATH_TO_FILES}/{current_table[TABLE]}.csv'
    csv_headers = current_table[HEADERS]
    headers = csv_headers.strip().split(',')
    placeholders = ','.join(['%s'] * len(headers))
    dt_field = current_table[DATEFIELD]

    for chunk in pd.read_csv(
            csv_file,
            chunksize=CHUNK_SIZE,
            usecols=headers,
            encoding='utf-8'):
        chunk[dt_field] = pd.to_datetime(chunk[dt_field])

        data_tuples = [tuple(row) for row in chunk.to_numpy()]

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(current_table[TABLE]),
            sql.SQL(csv_headers),
            sql.SQL(placeholders)
        )
        cur.executemany(insert_query, data_tuples)
        conn.commit()

cur.close()
conn.close()
