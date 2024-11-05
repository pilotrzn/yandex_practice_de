def find_two_indexes(data: list, expected_sum: int):
    length = len(data)
    solutions = []
    for i in range(0, length):
        for y in range(i + 1, length):
            if data[i] + data[y] == expected_sum:
                solutions.append((i, y))
    return solutions


if __name__ == '__main__':
    data = [1, 2, 3, 4, 5, 6, 7, 11]
    expected_sum = 10
    print(find_two_indexes(data, expected_sum))