import sys


def index():
    probe_arr = list(map(int, input().strip().split()))
    # probe_arr = [1, 5, 10, 11]
    check_value = int(sys.stdin.readline().rstrip())
    # check_value = 15
    print(check_element_in_list(check_value, probe_arr))


def check_element_in_list(check_value: int, probe_arr: list) -> int:
    first: int = 0
    last: int = len(probe_arr) - 1
    if check_value < probe_arr[first]:
        result = first
    if check_value > probe_arr[last]:
        result = last + 1

    for index, item in enumerate(probe_arr):
        if item >= check_value:
            result = index
            break
    return result


if __name__ == '__main__':
    index()
