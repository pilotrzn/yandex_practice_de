def pay_bills(month, bills):
    # Ваш код здесь
    if month % 3 == 0:
        return bills[1:len(bills) - 1]
    else:
        return bills[::len(bills) - 1]
    


# Вызов функции:
print(pay_bills(7, ['Интернет', 'Коммуналка', 'Телефон', 'Страховка']))