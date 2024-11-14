def main():
    message = list(map(str, input()))
    print(is_correct_bracket_seq((message)))


def is_correct_bracket_seq(message_string: str):
    # пустая строка
    if not len(message_string):
        return True
    # если нечетное число символов
    if len(message_string) % 2:
        return False

    brackets = {
        '(': ')',
        '{': '}',
        '[': ']'
    }
    stack = []
    for symb in message_string:
        if symb in brackets.keys():
            stack.append(symb)
        elif len(stack) and brackets[stack.pop()] != symb:
            return False
    return not stack


if __name__ == '__main__':
    main()
