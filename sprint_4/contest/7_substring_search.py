def substring_search(message):
    symb_count = 0
    finded = []
    for symb in message:
        if symb not in finded:
            finded.append(symb)
            symb_count = max(symb_count, len(finded))
        else:
            finded = finded[finded.index(symb) + 1:]
            finded.append(symb)
    return symb_count


if __name__ == '__main__':
    # data = 'abcdeabcabcdbb'
    data = list(map(str, input()))
    print(substring_search(data))
