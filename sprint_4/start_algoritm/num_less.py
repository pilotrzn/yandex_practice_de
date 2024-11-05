# Количество чисел меньше текущего
import random


def list_gen() -> list:
    list_of_int = []
    for _ in range(0, 100):
        list_of_int.append(random.randint(0, 100))
    return list_of_int


def check_num_list(nums: list):
    check = []
    for i in range(len(nums)):
        count = 0
        for j in range(len(nums)):
            if nums[i] > nums[j]:
                count += 1
        check.append(count)
    return check


def main():
    # nums = list(map(int, input().strip().split()))
    nums = list_gen()
    print(*check_num_list(nums))


if __name__ == '__main__':
    main()