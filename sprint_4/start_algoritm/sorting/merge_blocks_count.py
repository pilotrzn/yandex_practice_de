def inputs():
    num = int(input().strip())
    arr_list = [int] * num
    arr_list = list(map(int, input().strip().split()))
    return num, arr_list


def merge_blocks_count(arr_list: list):
    ordered_array: dict[int, int] = {
        order: arr_list[order] for order in range(0, len(arr_list))}
    blocks = 0
    start_val = 0
    for order, value in ordered_array.items():
        start_val = max(start_val, value)
        if start_val == order:
            blocks += 1
    return blocks


if __name__ == '__main__':
    num, arr_list = inputs()
    print(merge_blocks_count(arr_list))

