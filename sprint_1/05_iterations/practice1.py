
def print_pack_report(starting_value):
    for value in range(starting_value,0,-1):
        if value % 15 == 0: #and value % 3 == 0:
            print(f'{value} - расфасуем по 3 или по 5')
        elif value % 5 == 0:
            print(f'{value} - расфасуем по 5')
        elif value % 3 == 0:
            print(f'{value} - расфасуем по 3')
        else:
            print(f'{value} - не заказываем!')

print_pack_report(31)   