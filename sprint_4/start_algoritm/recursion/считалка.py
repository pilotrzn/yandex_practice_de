import sys


def input():
    members = int(sys.stdin.readline().rstrip())
    tacts = int(sys.stdin.readline().rstrip())
    return members, tacts


def get_winner(members: int, tacts: int) -> int:
    # если такт 1 то вернем 1 участника
    if members == 1:
        return 1
    else:
        winner = (get_winner(members - 1, tacts) + tacts - 1) % members + 1

        return winner


if __name__ == '__main__':
    # members = int(sys.stdin.readline().rstrip())
    # tacts = int(sys.stdin.readline().rstrip())
    print(get_winner(5, 3))



    # (1 + 16 - 1) % 1 + 1 = 17