import os


LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'


if LOCAL:
    class Node:
        def __init__(self, value, next_item=None):
            self.value = value
            self.next_item = next_item


def solution(node: Node, idx):
    # удалить саму голову - возвращаем следующий
    if idx == 0:
        return node.next_item

    # выбираем ноду, которую меняем
    node_to_change = node
    for _ in range(0, idx - 1):
        # исключаем вариант, когда индекс за пределами списка
        if node_to_change.next_item is None:
            return node
        node_to_change = node_to_change.next_item

    if node_to_change.next_item is not None:
        node_to_change.next_item = node_to_change.next_item.next_item
    # если удалялся не 0 узел, возвращаем голову
    return node


def test():
    node3 = Node("Задача 4: Обследовать грунт в радиусе 3 м", None)
    node2 = Node("Задача 3: Измерить температуру атмосферы", node3)
    node1 = Node("Задача 2: Пробурить скважину глубиной 0.5 м", node2)
    node0 = Node("Задача 1: Фотосъёмка 360°", node1)

    new_head = solution(node0, 1)
    # Выражение, начинающееся с ключевого слова assert,
    # проверяет, что утверждение в выражении истинно.
    # Если утверждение ложно - в этом месте возникнет ошибка.
    assert new_head is node0
    assert new_head.next_item is node2
    assert new_head.next_item.next_item is node3
    assert new_head.next_item.next_item.next_item is None
    # result is node0 -> node2 -> node3


if __name__ == '__main__':
    test()
