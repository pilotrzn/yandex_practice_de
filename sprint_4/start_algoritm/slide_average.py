import sys


def inputs():
    count_mes = int(sys.stdin.readline().rstrip())

    measures = [None] * count_mes
    measures = list(map(int, input().strip().split()))
    k = int(input())
    result = []
    i = 0
    ln = len(measures) - k + 1
    while i < ln:
        result.append(str((summ(measures[i:i + k], k))))
        i += 1

    print(" ".join(result))


def summ(measuses_list: list, k: int):
    sum_meas = sum(measuses_list)
    return sum_meas / k


if __name__ == '__main__':
    inputs()
