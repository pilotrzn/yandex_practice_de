def valid_mountain_array(mountain: list) -> bool:
    if len(mountain) < 3:
        return False
    # index of  max value
    top = mountain.index(max(mountain))
    one_way = (top not in (0, len(mountain) - 1))
    up = all(right - left > 0 for left, right in zip(mountain[:top],
                                                     mountain[1:top + 1]))
    down = all(right - left < 0 for left, right in zip(mountain[top:],
                                                       mountain[top + 1:]))
    return one_way and up and down


def main():
    moun = list(map(int, input().strip().split()))
    print(valid_mountain_array(moun))


if __name__ == '__main__':
    main()
