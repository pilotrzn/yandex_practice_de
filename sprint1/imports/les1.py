# Из модуля decimal импортируйте тип данных Decimal и параметр getcontext.
from decimal import Decimal, getcontext
# Из модуля math импортируйте константу "пи".
from math import pi
# Приведите константу "пи" к типу Decimal.

pi = Decimal(str(pi))
# Помните, что Decimal() принимает строку, а константа "пи" - это число.
# Установите необходимую точность для вычислений.
getcontext().prec = 10

# Объявите функцию ellipse_area() с двумя параметрами.
def ellipse_area(large_os, small_os):
    print(pi)
    return pi * large_os * small_os

# Объявите три переменные типа Decimal - 
# они должны хранить длины полуосей эллипса и глубину пруда.
l_os = 2.5
s_os = 1.75
large_os = Decimal(str(l_os))
small_os = Decimal(str(s_os))
depth = Decimal('0.35')
print(type(s_os), type(small_os), pi * l_os)

# Вызовите функцию ellipse_area(), в аргументах передайте длины полуосей эллипса.
area = ellipse_area(large_os,small_os)

# Вычислите объём пруда: площадь * глубина.
vol = area * depth
print('Площадь эллипса:', area, 'кв.м.')
print('Объем воды для наполнения пруда:',vol,'куб.м.')