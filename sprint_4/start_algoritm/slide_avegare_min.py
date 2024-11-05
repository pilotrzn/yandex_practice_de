# Импортируем число, заведомо большее, чем любая сумма элементов среза.
from sys import maxsize


def find_min_slice_sum(data, elements_in_slice):
    min_sum = maxsize
    for index in range(len(data) - elements_in_slice + 1):
        temp_sum = 0
        for slice_index in range(elements_in_slice):
            temp_sum += data[index + slice_index]
        min_sum = min(min_sum, temp_sum)
    return min_sum


if __name__ == '__main__':
    data = [5, -3, -2, 10, 2, 7, 1, -6, 13]
    elements_in_slice = 4
    print(find_min_slice_sum(data, elements_in_slice))