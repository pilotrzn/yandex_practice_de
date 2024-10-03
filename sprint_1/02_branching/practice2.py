def count_tiles(depth, length, width=None):
    if width is None:
        width = length

    width_side = 2 * width * depth
    length_side = 2 * length * depth
    bottom_tiles = length * width
    total = width_side + length_side + bottom_tiles

    return total

# Передайте в функцию нужный параметр и напишите её код.


def make_phrase(num):
    tiles = 'плиток'
    if 14 >= num >= 11:
        tiles = 'плиток'
    elif (num % 10) == 1:
        tiles = 'плитку'
    elif 2 <= (num % 10) <= 4:
        tiles = 'плитки'
    else:
        tiles = 'плиток'

    return str(num) + ' ' + tiles


total_tiles = count_tiles(5, 3, 2)
# Выведите на экран нужное сообщение.
print('Для строительства бассейна нужно заготовить', make_phrase(total_tiles))
