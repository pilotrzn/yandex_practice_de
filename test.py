# Из модуля decimal импортируйте тип данных Decimal и параметр getcontext.
from decimal import Decimal, getcontext
from math import pi

pi = Decimal(str(pi))
getcontext().prec = 10

# Объявите функцию ellipse_area() с двумя параметрами.
def ellipse_area(large_os, small_os):

    print(id(small_os))
    small_os = large_os * 2
    print(id(small_os), small_os)
    return pi * large_os * small_os


large_os = Decimal('2.5')
small_os = Decimal('1.75')
depth = Decimal('0.35')


area = ellipse_area(large_os,small_os)
vol = area * depth
print('Площадь эллипса:', area, 'кв.м.')
print('Объем воды для наполнения пруда:',vol,'куб.м.')
print(small_os,large_os)