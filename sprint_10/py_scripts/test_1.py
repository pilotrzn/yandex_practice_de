TABLE = 'table'
HEADERS = 'headers'
TABLES = [
    {
        TABLE: 'customer_research',
        HEADERS: 'date_id,category_id,geo_id,sales_qty,sales_amt'
    },
    {
        TABLE: 'user_order_log',
        HEADERS: 'id,date_time,city_id,city_name,customer_id,first_name,'
        'last_name,item_id,item_name,quantity,payment_amount'
    },
    {
        TABLE: 'user_activity_log',
        HEADERS: 'id,date_time,action_id,customer_id,quantity'
    }
]
PATH_TO_FILES = '/lessons/2. Анализ вводных по задаче/7. Использование файлов и подключение к БД/Задание 1/stage'


for current_table in TABLES:
    csv_file = f'{PATH_TO_FILES}/{current_table[TABLE]}.csv'
    csv_headers = current_table[HEADERS]
    print(csv_file)
    print(len(csv_file))
