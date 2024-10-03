from math import sqrt
from typing import Optional


def add_numbers(item1: int, item2: int) -> int:
    return item1 + item2


def calculate_square_root(number: float) -> float:
    return sqrt(number)


def calc(your_number: float) -> Optional[str]:
    if your_number <= 0:
        calc_square = None
    else:
        calc_square = calculate_square_root(your_number)
    return str.format('Мы вычислили квадратный корень из '
                      'введённого вами числа. '
                      'Это будет: {}', calc_square)


var1 = 10
var2 = 5

print('Сумма чисел: ', add_numbers(var1, var2))

print(calc(100))
print(calc(0))
