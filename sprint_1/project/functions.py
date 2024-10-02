from datetime import datetime, date
from decimal import Decimal as dec
from pathlib import Path
import json


DATE_FORMAT = '%Y-%m-%d'
KEY_AMOUNT = 'amount'
KEY_EXPIRATION = 'expiration_date'


def check_date(var_date: str):
    result = None
    if var_date != '':
        result = datetime.strptime(var_date, DATE_FORMAT).date()
    return result


def add(items: dict, title: str, amount: str, expiration_date: str = ''):
    dt_exp_date = check_date(expiration_date)
    dict_properties = {
        KEY_AMOUNT: amount,
        KEY_EXPIRATION: dt_exp_date
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
        len_splitstr = len(splitstr) - 2
    except ValueError:
        False
    count = splitstr[len_splitstr]
    add(items, ' '.join(splitstr[:len_splitstr]), count, str(s_date))
    print(items)


def find(items: dict, needle: str):
    n_l = needle.lower()
    return [value for value in items.keys() if value.lower().count(n_l) > 0]


def amount(items: dict, needle: str) -> dec:
    sum_amount = 0
    # Поиск продукта
    titles = find(items, needle)
    for title in titles:
        for item in items[title]:
            sum_amount += item[KEY_AMOUNT]
    return dec(sum_amount)


def amount2(items, needle):
    total_amount = 0
    titles_find = find(items, needle)
    if len(titles_find) == 0:
        return dec(total_amount)
    for title in items:
        if title in titles_find:
            title_values = dict.get(items, title)
            for every_dict in title_values:
                total_amount += every_dict[KEY_AMOUNT]
    return dec(total_amount)


def expire(items: dict, in_advance_days: int = 0) -> list:
    expire_product = []
    tday = date.today()
    for title in items:
        sum_expired = 0
        for item in items[title]:
            if item[KEY_EXPIRATION]:
                if (item[KEY_EXPIRATION] - tday).days <= in_advance_days:
                    sum_expired += item[KEY_AMOUNT]
            if sum_expired != 0:
                expire_product.append((title, sum_expired))
    return expire_product


def export_to_json(items: dict):
    workfolder = Path('.').joinpath('yandex_pract').joinpath('sprint_1')
    file_path = Path(workfolder).joinpath('project').joinpath('rfrgr.json')
    jsondata = json.dumps(items, ensure_ascii=False, default=str, indent=1)
    with open(file_path, 'w') as result:
        result.write(jsondata)
