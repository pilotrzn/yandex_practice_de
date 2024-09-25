from datetime import datetime , date
from decimal import Decimal as dec


DATE_FORMAT = '%Y-%m-%d'


def add(items: dict, title: str, amount: dec, expiration_date: str = None):
    dt_exp_date = datetime.strptime(expiration_date, DATE_FORMAT).date() if expiration_date else expiration_date
    dict_properties = {
        'amount': amount, 
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

def amount2(items, needle):
    total_amount = 0 
    titles_find = find(items, needle)

    if len(titles_find) == 0:
        return dec(total_amount)
    
    for title in items:
        if title in titles_find:
            title_values = dict.get(items, title)
            print(title_values)
        
            for every_dict in title_values:
                total_amount += every_dict['amount']
                
    return dec(total_amount)


def expire(items: dict, in_advance_days: int = 0):
    expire_product = []
    for title in items:
        sum_expired = 0
        for item in items[title]:           
            if item['expiration_date'] and (item['expiration_date'] - date.today()).days <= in_advance_days:
                    sum_expired += item['amount']
        if sum_expired != 0:
            expire_product.append((title,sum_expired))     
    return expire_product


