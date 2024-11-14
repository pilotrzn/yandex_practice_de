example_array = [6, 5, 3, 1, 8, 7, 2, 4, 2, 2]
# example_array = [2, 3, 1, 4, 5, 6, 7, 8]


def bubble_sort(array: list) -> list:
    # сортировка методом пузырька
    arr_size = len(array)
    steps = 0
    while arr_size != 0:
        replace = False
        for i in range(arr_size - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                replace = True
                steps += 1
        if not (replace):
            break
        arr_size -= 1
    print(steps)
    return array


def bubble_sort_while(array: list) -> list:
    # сортировка методом пузырька
    arr_size = len(array)
    replace = True
    while replace:
        replace = False
        for i in range(arr_size - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = (
                    array[i + 1], array[i]
                    )
                replace = True
        arr_size -= 1
    return array


print(bubble_sort(example_array))
