# id посылки = 123761471
# google_doc = https://docs.google.com/document/d/1lJMxsBK2GK_tv-bZuPohJ8qCY_7R2xivdrGsLGRYFUM/edit?usp=sharing


def platform_count(robots_weigth: list[int], limit: int) -> int:
    """Determination of the minimum number of transport platforms
        or the transportation of all robots

    Args:
        robots_weigth (list[int]): Array(list) with robot weights
        limit (int): Maximum load capacity of the platform

    Returns:
        int: Required number of platforms for transportation
    """
    transporter_count = 0
    left_pointer = 0
    right_pointer = len(robots_weigth) - 1
    # Sort array
    robots_weigth = sorted(robots_weigth)
    while left_pointer <= right_pointer:
        weight = robots_weigth[left_pointer] + robots_weigth[right_pointer]
        if weight <= limit:
            left_pointer += 1
        transporter_count += 1
        right_pointer -= 1
    return transporter_count


def inputs() -> tuple[list[int], int]:
    """Data entry

    Returns:
        tuple[list[int], int]: Returns a tuple from the list of platform
        weights and the limit value per platform
    """
    robots_weigth = list(map(int, input().strip().split()))
    limit = int(input().strip())
    return robots_weigth, limit


if __name__ == '__main__':
    robots_weigth, limit = inputs()
    print(platform_count(robots_weigth=robots_weigth, limit=limit))
