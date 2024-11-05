wins = [1223125, 2128437, 2128500, 2741001, 4567687, 4567890, 7495938, 9314543]

wins = [i for i in range(0, 1025)]


def find_element(sorted_numbers, element):
    """Находит индекс element в отсортированном списке sorted_numbers."""
    left = 0
    count = 0
    right = len(sorted_numbers)
    while left <= right:
        mid = (left + right) // 2
        if sorted_numbers[mid] == element:
            return mid, count
        if sorted_numbers[mid] < element:
            left = mid + 1
        if sorted_numbers[mid] > element:
            right = mid - 1
        count += 1
    return None


print(find_element(wins, 3000))
