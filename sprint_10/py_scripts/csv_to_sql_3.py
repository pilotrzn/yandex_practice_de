import numpy as np
import psycopg2
from psycopg2 import sql
from datetime import datetime

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

# Чтение CSV-файла с использованием numpy
# Указываем dtype=None для автоматического определения типов данных
data = np.genfromtxt(csv_file_path, delimiter=',', skip_header=1, dtype=None, encoding='utf-8')

# Получение заголовков (названий колонок)
with open(csv_file_path, 'r', encoding='utf-8') as f:
    headers = f.readline().strip().split(',')

# Разделение данных на чанки
chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Создание SQL-запроса для вставки данных
insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
    sql.Identifier(table_name),
    sql.SQL(',').join(map(sql.Identifier, headers)),
    sql.SQL(',').join([sql.Placeholder()] * len(headers))
)

# Функция для преобразования строки в datetime
def parse_datetime(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')  # Формат datetime в CSV
    except ValueError:
        return None  # Если преобразование не удалось

# Вставка данных по чанкам
for chunk in chunks:
    # Преобразование numpy массива в список кортежей с обработкой datetime
    data_tuples = []
    for row in chunk:
        # Преобразуем каждое значение в строку и обрабатываем datetime
        processed_row = []
        for value in row:
            if isinstance(value, str) and ':' in value:  # Проверяем, может ли это быть datetime
                processed_value = parse_datetime(value)
            else:
                processed_value = value
            processed_row.append(processed_value)
        data_tuples.append(tuple(processed_row))
    
    # Вставка данных
    cursor.executemany(insert_query, data_tuples)
    conn.commit()

# Закрытие соединения
cursor.close()
conn.close()