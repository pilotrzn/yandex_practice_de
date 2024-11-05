class Box:

    def __init__(self, size, inner_items=None):
        self.size = size
        self.inner_items = inner_items

    def __repr__(self):
        # При распечатке объекта через print()
        # будет выводиться свойство size - размер коробки.
        return self.size


def disassemble_boxes(box):
    """Функция разборки коробок."""
    items_for_disassemble = [box]

    # Пока список items_for_disassemble не пуст - выполняем цикл.
    while items_for_disassemble:
        # Извлекаем последний элемент из списка.
        element_to_disassemble = items_for_disassemble.pop()
        # Получаем из текущего элемента вложенные элементы.
        inner_items = element_to_disassemble.inner_items
        # Если вложенные элементы существуют...
        if inner_items is not None:
            # ...добавляем их в список. 
            # Элементов может быть несколько, поэтому применяем extend().
            items_for_disassemble.extend(inner_items)
            print(f'Взяли коробку размера {element_to_disassemble.size}, '
                  f'внутри: {inner_items}.')
        else:
            print(f'В коробке размера {element_to_disassemble.size} '
                  'больше ничего нет.')


if __name__ == '__main__':
    # Создаём четыре маленькие коробки: четыре объекта класса Box. 
    # В них ничего нет.
    small_boxes = [Box(size='S') for _ in range(4)]
    # Создаём коробку среднего размера, пустую:
    middle_box_empty = Box(size='M')
    # Создаём ещё одну среднюю коробку, в неё кладём четыре маленькие:
    middle_box_full = Box(size='M', inner_items=small_boxes)
    # Создаём большую коробку, в неё вкладываем две средние:
    large_box = Box(size='L', inner_items=[middle_box_empty, middle_box_full])
    # Отправляем большую коробку в функцию-разбиратель:
    disassemble_boxes(large_box)