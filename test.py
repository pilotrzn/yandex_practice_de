
from decimal import Decimal, getcontext
from math import pi

pi = Decimal(str(pi))
getcontext().prec = 10

def ellipse_area(large_os, small_os):
    # номер ячейки в памяти
    print(id(small_os))
    # меняем значение
    small_os = large_os * 2
    # номер ячейки в памяти
    print(id(small_os), small_os)
    return pi * large_os * small_os

large_os = Decimal('2.5')
small_os = Decimal('1.75')
depth = Decimal('0.35')

area = ellipse_area(large_os,small_os)
vol = area * depth
print('Площадь эллипса:', area, 'кв.м.')
print('Объем воды для наполнения пруда:',vol,'куб.м.')
# значения не поменялись
print(small_os,large_os)