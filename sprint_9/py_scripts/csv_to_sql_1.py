import pandas as pd
import psycopg2
from psycopg2 import sql

# Параметры подключения к базе данных
db_config = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

# Путь к CSV-файлу
csv_file_path = 'path/to/your/file.csv'

# Имя таблицы в PostgreSQL
table_name = 'your_table_name'

# Размер чанка (количество строк для вставки за один раз)
chunk_size = 1000

# Подключение к базе данных
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Чтение CSV-файла по частям
for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
    # Преобразование DataFrame в список кортежей
    data_tuples = [tuple(x) for x in chunk.to_numpy()]
    
    # Получение названий колонок
    columns = ','.join(chunk.columns)
    
    # Создание SQL-запроса для вставки данных
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(columns),
        sql.SQL(',').join(map(sql.Placeholder, chunk.columns))
    )
    
    # Вставка данных
    cursor.executemany(insert_query, data_tuples)
    conn.commit()

# Закрытие соединения
cursor.close()
conn.close()