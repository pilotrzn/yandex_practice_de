import sys


def zip():
    arr_size = int(sys.stdin.readline().rstrip())
    first_arr = [None] * arr_size
    second_arr = [None] * arr_size
    zipper = []
    first_arr = list(input().strip().split())
    second_arr = list(input().strip().split())

    for index in range(arr_size):
        zipper.append(first_arr[index])
        zipper.append(second_arr[index])

    print(" ".join(zipper))


if __name__ == '__main__':
    zip()
