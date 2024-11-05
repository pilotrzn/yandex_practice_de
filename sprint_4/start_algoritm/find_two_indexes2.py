def find_two_indexes(data, expected_result):
    # В начале работы 
    solutions = []
    # - левый указатель указывает на первый элемент списка (с индексом 0):
    left_pointer = 0
    # - правый указатель указывает на последний элемент списка. 
    # Индекс этого элемента на единицу меньше длины списка.
    right_pointer = len(data) - 1
    # Пока индекс левого указателя меньше индекса правого указателя.
    while left_pointer < right_pointer:
        # Считаем сумму двух элементов.
        sum = data[left_pointer] + data[right_pointer]
        # Если она совпадает с искомой...
        if sum == expected_result:
            solutions.append((left_pointer, right_pointer))
            right_pointer -= 1
            left_pointer += 1
        # Если сумма больше искомой, то...
        if sum > expected_result:
            right_pointer -= 1
        if sum < expected_result:
            left_pointer += 1
    return solutions


if __name__ == '__main__':
    data = [1, 2, 3, 4, 5, 6, 7, 11]
    expected_result = 10
    print(*find_two_indexes(data, expected_result))