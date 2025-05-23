def insertion_sort(arr):
    # Проходим по всем элементам массива, начиная со второго.
    for i in range(1, len(arr)):
        # Сохраняем текущий элемент в переменную current.
        current = arr[i]
        # Сохраняем индекс предыдущего элемента 
        # в переменную prev (от previous - предыдущий).
        prev = i - 1
        # Сравниваем current с предыдущим элементом 
        # и двигаем предыдущий элемент на одну позицию вправо, 
        # пока он больше current и не достигнуто начало массива.
        while prev >= 0 and arr[prev] > current:
            arr[prev + 1] = arr[prev]
            prev -= 1
        # Вставляем current в отсортированную часть массива на нужное место.
        arr[prev + 1] = current
        print(f'Шаг {i}, отсортировано элементов: {i + 1}, {arr}')


insertion_sort([2, 9, 11, 7, 1])