from datetime import datetime


DATE_FORMAT = '%d.%m.%Y'
GOOD_KEY = 'good'
BAD_KEY = 'bad'


def validate_record(name, burn_date):
    try:
        bool(datetime.strptime(burn_date, DATE_FORMAT).date())
        return True
    except ValueError:
        print(f'Некорректный формат даты в записи: {name}, {burn_date}')
        return False


def process_people(data: list):
    good_count = 0
    bad_count = 0
    result = dict()
    for name, burn_date in data:
        if validate_record(name=name, burn_date=burn_date):
            good_count += 1
        else:
            bad_count += 1
    result[GOOD_KEY] = good_count
    result[BAD_KEY] = bad_count
    print(f'Корректных записей: {good_count}')
    print(f'Некорректных записей: {bad_count}')
    return result


data = [
    ('Иван Иванов', '10.01.2004'),
    ('Пётр Петров', '15.03.1956'),
    ('Зинаида Зеленая', '6 февраля 1997'),
    ('Елена Ленина', 'Второе мая тысяча девятьсот восемьдесят пятого'),
    ('Кирилл Кириллов', '26/11/2003')
]

statistics = process_people(data)
