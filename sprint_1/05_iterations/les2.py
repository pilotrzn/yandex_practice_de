from random import randint

# Начальная температура чая
current_temperature = 85

# Объявите цикл while

while current_temperature > 60:
    down_temp = randint(1, 3)
    current_temperature -= down_temp
    print(f'Чай остыл ещё на {down_temp} °C. Текущая температура: {current_temperature} °C')

print('Время пить чай! ')
