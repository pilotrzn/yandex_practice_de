def duble():
    length = int(input().strip())
    result = ['_'] * length
    probe_arr = list(input().strip().split())
    index = 0
    for probe in probe_arr:
        if probe not in result:
            result[index] = probe
            index += 1
    return result


if __name__ == '__main__':
    print(*duble())
