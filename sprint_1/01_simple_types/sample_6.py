bool_true = True     # Булево значение.
bool_false = False   # Булево значение.
int_null = 0         # Число.
int_one = 1          # Число.
int_100 = 100        # Число.
int_negative = -100  # Число.
float_pi = 3.14      # Число с плавающей точкой.

print('Вместо True -', int(bool_true))   # Приводим bool к числу.
print('Вместо False -', int(bool_false)) # Приводим bool к числу.

print('Вместо 0 -', bool(int_null))         # Приводим число к bool.
print('Вместо 1 -', bool(int_one))          # Приводим число к bool.
print('Вместо 100 -', bool(int_100))        # Приводим число к bool.
print('Вместо -100 -', bool(int_negative))  # Приводим число к bool.
print('Вместо 3.14 -', bool(float_pi))      # Приводим число к bool.


def rectangle_area(length, width):
    return length * width


area_1 = rectangle_area(5, 10)
area_2 = rectangle_area(7, 7)

print('Площадь первой грядки меньше второй?', area_1 < area_2)
print('Площадь первой грядки равна второй?', area_1 == area_2)
print('Площадь первой грядки больше второй?', area_1 > area_2)
