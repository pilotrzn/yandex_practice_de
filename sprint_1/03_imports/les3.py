from datetime import datetime as dt


def timedelta_days(datetime_str_1, datetime_str_2):
    # Напишите тело функции.
    format = '%Y/%m/%d %H:%M:%S'
    d_diff = dt.strptime(
        datetime_str_2, format) - dt.strptime(datetime_str_1, format
                                              )
    return d_diff.days


difference = timedelta_days('2019/05/10 00:00:00', '2019/10/04 00:00:00')

print('От начала посевной до начала сбора урожая прошло', difference, 'дней.')
