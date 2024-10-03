# Вместо многоточия укажите необходимые параметры.
def count_tiles(depth, length, width=None):
    # Опишите условие, когда ширина бассейна не указана.
    if width is None:
        width = length

    # Посчитайте, сколько понадобится плиток для стенок и дна бассейна.
    plit_cnt = 2 * ((length * depth) + (width * depth)) + length * width

    # Верните результат работы функции.
    return plit_cnt


total_tiles = count_tiles(1, 1, 1)
print('Общее количество плиток для строительства бассейна:', total_tiles)
