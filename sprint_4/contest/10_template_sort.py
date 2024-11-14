import sys


def inputs():
    container_size = int(sys.stdin.readline().rstrip())
    container_list = [int] * container_size
    container_list = list(map(int, input().strip().split()))
    template_size = int(sys.stdin.readline().rstrip())
    template = [int] * template_size
    template = list(map(int, input().strip().split()))
    return template, container_list


def template_sorting(template: list, container: list):
    meets: dict[int, int] = {num: container.count(num) for num in template}
    other_items: list[int] = [
        element for element in container if element not in template]
    result: list[int] = [item for item in template for _ in range(meets[item])]
    other_items.sort()
    result.extend(other_items)
    return result


if __name__ == '__main__':
    template, container_list = inputs()
    print(*template_sorting(template, container_list))
