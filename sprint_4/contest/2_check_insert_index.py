def inputs() -> tuple[list[int], int]:
    probe_arr = list(map(int, input().strip().split()))
    check_value = int(input().strip())
    return probe_arr, check_value


def check_element_in_list(probe_arr: list, check_value: int) -> int:
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
    probe_arr, check_value = inputs()
    print(check_element_in_list(probe_arr, check_value))
