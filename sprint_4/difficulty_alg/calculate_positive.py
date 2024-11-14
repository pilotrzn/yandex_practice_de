days_temp = [-1, -4, 8, -7, 3, 0, 1, -7, -7, 0, 0, -4, 1, 8, 1, -5, 4, 0, 7, 1]


class Sequence:

    def __init__(self, sequence):
        # Список с накопительной суммой, для первого элемента она равна 0.
        self.cumulative_sums = [0]
        count = 0
        # Вычисляем накопительную сумму для массива:
        for i in sequence:
            # Если нашлось положительное значение...
            if i > 0:
                # ...увеличиваем счётчик:
                count += 1
            # Добавляем очередной элемент к списку с накопительной суммой.
            self.cumulative_sums.append(count)

    def calculate_positive(self, left, right):
        # Чтобы посчитать количество положительных значений
        # на любом участке массива, просто выполняем вычитание.
        return self.cumulative_sums[right] - self.cumulative_sums[left]


s = Sequence(days_temp)
# Покажет количество положительных чисел в интервале от 10 до 19 -
# с 10-го по 18-й элемент включительно.
print(s.calculate_positive(10, 19))
