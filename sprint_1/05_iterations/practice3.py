def print_multiplication_table():
    for mult1 in range(1,10):
        for mult2 in range(1,10):
            mult = mult1 * mult2
            print(f'{mult1} * {mult2} = {mult}')
        print('-' * 10)

print_multiplication_table()