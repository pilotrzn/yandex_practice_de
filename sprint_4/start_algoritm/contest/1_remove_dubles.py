import sys


def duble():
    length = int(sys.stdin.readline().rstrip())
    result = ['_'] * length
    probe_arr = list(input().strip().split())
    index = 0
    for probe in probe_arr:
        if probe not in result:
            result[index] = probe
            index += 1

    print(" ".join(str(result)))


if __name__ == '__main__':
    duble()
