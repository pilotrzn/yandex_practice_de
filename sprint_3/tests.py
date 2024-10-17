from datetime import datetime
import calendar


DATE_FORMAT = '%Y.%m.%d'


def month_iter(year, month):
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        yield year, month, day


for year, month, day in month_iter(2021, 10):
    date_str = f'{year}.{month}.{day}'
    date_object = datetime.strptime(date_str, DATE_FORMAT).date()
    print(f'{date_object} - {date_object.weekday()}')


# Что хорошего есть в библиотеке math?
print(print.__doc__)
