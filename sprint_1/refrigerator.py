# imports
from datetime import datetime as dt, timedelta as tdlt,date
from decimal import Decimal as dec, getcontext
getcontext().prec = 3


# constants
DATE_FORMAT = '%Y-%m-%d'
STR_SPLITTER = '; '
STR_NOTE = 'Яйца перепелиные; 10; 2024-10-01'
# vars
goods = {}


def add(items, title, amount, expiration_date=None):
    dt_exp_date = None if expiration_date == None else dt.strptime(expiration_date, DATE_FORMAT).date()
    dict_properties = {
        'amount': dec(str(amount)), # Привожу через str, чтобы не получать приближенное число, типа 0.49999000000....
        'expiration_date': dt_exp_date
    }
    if title not in items:
        items[title] = [dict_properties]
    else:
        items[title].append(dict_properties)

def add_by_note2(items, note):
    splitstr = note.split()
    check_value = splitstr[len(splitstr)-1]

    try:
        res = bool(dt.strptime(check_value, DATE_FORMAT).date())
    except ValueError:
        res = False

    if res:
        s_date = check_value
        cnt = splitstr[len(splitstr)-2]
        splitstr.pop(len(splitstr)-1)
        splitstr.pop(len(splitstr)-1)
    else:
        cnt = splitstr[len(splitstr)-1]
        splitstr.pop(len(splitstr)-1)
        s_date = None

    title = ' '.join(splitstr)   
    add(items, title, cnt, s_date)
    print(items)


def find(items, needle):
    return [ value for value in items.keys() if value.lower().count(needle.lower()) > 0 ]
    
def amount(items, needle):
    sum_amount = 0
    # Поиск продукта
    titles = find(items, needle)
    for title in titles:
            for item in items[title]:
                sum_amount += item['amount']
    return dec(sum_amount)


def expire(items, in_advance_days=0):
    expire_product = []
    d_today = date.today()
    for title in items:
        sum_expired = 0
        for item in items[title]:           
            if item['expiration_date']:
                if (item['expiration_date'] - d_today).days <= in_advance_days:
                        sum_expired += item['amount']
        if sum_expired != 0:
            expire_product.append((title,sum_expired))     
    return expire_product

add(goods, 'Пельмени универсальные', 2, '2024-10-10')
add(goods, 'Вода', 0.5)
add(goods, 'Яйца куриные', 20, '2024-09-16')
add(goods, 'Яйца куриные', 4, '2024-09-17')
add(goods, 'Пельмени универсальные', 0.5, '2025-01-10')
add(goods, 'Яйца перепелиные', 10, '2024-09-20')
add(goods, 'Колбаса', 0.60, '2024-09-24')
add(goods, 'Продукт_1', 12, '2024-09-17' )
add(goods, 'Продукт_2', 10, '2024-09-19' )
add(goods, 'Продукт_3', 3, '2024-09-18' )
add(goods, 'Продукт_4', 5, '2024-11-10' )

# add_by_note(goods, STR_NOTE)

# print(goods)

# print(find(goods,'яйц'))

# print(amount(goods,'яйц'))

# print(amount(goods,'x'))
print(expire(goods))

# add_by_note2({},'Яйца гусиные №1 4 2024-11-10')
# add_by_note2({},'Яйца гусиные №1 1.5')
# print(goods)