import time
from random import randint


start_time = time.time()

# Количество элементов установим равным 500 000.
DATA_SIZE = 500000
MAX_RAND_NUMBER = 10000000

# Теперь data - это не список, а множество. Скобки-то фигурные!
data = {randint(1, MAX_RAND_NUMBER) for _ in range(DATA_SIZE)}
print(f'Коллекция data сгенерирована за {time.time() - start_time} сек.')

match_counter = 0

# Будет выполнено 10 000 итераций цикла.
for _ in range(10000):
    new_item = randint(1, MAX_RAND_NUMBER)
    if new_item in data:
        match_counter += 1

print(f'Найдено совпадений: {match_counter}')
print(f'Объектов в data: {len(data)}')
print(f'Программа отработала за {time.time() - start_time} сек.')