class Matryoshka:
    def __init__(self, size, item=None):
        self.size = size
        self.inner_item = item


def disassemble_matryoshka(matryoshka):
    """Функция разборки матрёшки."""
    # Получаем вложенную матрёшку.
    inner_item = matryoshka.inner_item
    # Если вложенной матрёшки нет, значит, это была самая маленькая матрёшка
    # и работа закончена.
    if inner_item is None:
        print(f'Все матрёшки разобраны! Размер последней матрёшки:'
              f'{matryoshka.size}')
        return
    # Если вложенная матрёшка есть, печатаем информационное сообщение...
    print(f'Разобрали матрёшку размера {matryoshka.size}, разбираем дальше!')
    # ...и рекурсивно вызываем ту же функцию,
    # но аргументом в неё передаём объект, вложенный в текущий:
    disassemble_matryoshka(inner_item)


if __name__ == '__main__':
    # Создаём экземпляр матрёшки из трёх фигурок.
    big_matryoshka = Matryoshka('L', Matryoshka('M', Matryoshka('S')))
    # Передаём эту матрёшку на разборку.
    disassemble_matryoshka(big_matryoshka)
