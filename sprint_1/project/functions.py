from datetime import datetime , date
from decimal import Decimal as dec, getcontext


DATE_FORMAT = '%Y-%m-%d'


def test_add(items, title, amount, expiration_date = None):
    expiration = datetime.date(datetime.strptime(expiration_date, DATE_FORMAT)) #преобразем в дате в формат datetime и в формат date   
    if title not in  items:
        items[title] = [{'amount': amount, 'expiration_date': expiration}] # Добавляем в items title если его нет
    else:
        items[title].append ([{'amount': amount, 'expiration_date': expiration}]) #Применить append для добавления словаря с ключами 'amount' и 'expiration_date' в список для конкретного title.


def add(items: dict, title: str, amount: dec, expiration_date: str = None):
    dt_exp_date = datetime.strptime(expiration_date, DATE_FORMAT).date() if expiration_date else expiration_date
    dict_properties = {
        'amount': dec(str(amount)), # Привожу через str, чтобы не получать приближенное число, типа 0.49999000000....
        'expiration_date': dt_exp_date
    }

    if title not in items:
        items[title] = [dict_properties]
    else:
        items[title].append(dict_properties)


def add_by_note(items: dict, note: str):
    splitstr = note.split()
    # По-умолчанию делаем, будто не указана дата
    s_date = None
    len_splitstr = len(splitstr) - 1

    try:
        bool(datetime.strptime(splitstr[len_splitstr], DATE_FORMAT).date())
        s_date = splitstr[len_splitstr]
        len_splitstr = len(splitstr) - 2 # Если есть дата, то количество - предпоследний элемент
    except ValueError:
        False

    add(items, ' '.join(splitstr[:len_splitstr]), splitstr[len_splitstr], s_date)
    print(items)


def find(items: dict, needle: str):
    return [ value for value in items.keys() if value.lower().count(needle.lower()) > 0 ]

    
def amount(items: dict, needle: str):
    sum_amount = 0
    # Поиск продукта
    titles = find(items, needle)
    for title in titles:
            for item in items[title]:
                sum_amount += item['amount']
    return dec(sum_amount)


def expire(items: dict, in_advance_days: int = 0):
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


