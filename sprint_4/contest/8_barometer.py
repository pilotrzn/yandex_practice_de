import sys


def input():
    return int(sys.stdin.readline().rstrip())


def get_measure_count(version: int):
    if version in (0, 1):
        return 1
    return get_measure_count(version - 1) + get_measure_count(version - 2)


if __name__ == '__main__':
    version = input()
    print(get_measure_count(version))
