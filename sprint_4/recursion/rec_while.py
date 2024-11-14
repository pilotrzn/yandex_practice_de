class Matryoshka:

    def __init__(self, size, item=None):
        self.size = size
        self.inner_item = item


def disassemble_matryoshka(matryoshka):
    """Функция разборки матрёшки."""
    # В этом списке храним ту матрёшку,
    # которую цикл разбирает в текущей итерации.
    # В начале выполнения программы здесь хранится самая большая матрёшка.
    items_for_disassemble = [matryoshka]

    # Пока список items_for_disassemble не пуст, выполняем цикл.
    while items_for_disassemble:
        # Извлекаем последний (он же единственный) элемент из списка.
        element_to_disassemble = items_for_disassemble.pop()
        # Получаем из текущего элемента вложенный.
        inner_item = element_to_disassemble.inner_item
        # Если вложенный элемент существует...
        if inner_item is not None:
            # ...помещаем этот вложенный элемент в список.
            # Список был пуст, но полезно вспомнить, 
            # что метод append() добавляет новый элемент в конец списка.
            items_for_disassemble.append(inner_item)
            print(f'Разобрали матрёшку размера {element_to_disassemble.size}, разбираем дальше!')
    # Когда цикл выполнился, печатаем сообщение 
    # об окончании работы и данные последней матрёшки:
    print(f'Все матрёшки разобраны! Размер последней матрёшки: {element_to_disassemble.size}')


if __name__ == '__main__':
    big_matryoshka = Matryoshka('L', Matryoshka('M', Matryoshka('S')))
    disassemble_matryoshka(big_matryoshka)