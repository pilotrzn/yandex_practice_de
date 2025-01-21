from datetime import datetime as dt, timedelta as td


def get_weekday_name(weekday_number):
    if weekday_number == 0:
        return 'понедельник'
    elif weekday_number == 1:
        return 'вторник'
    elif weekday_number == 2:
        return 'среда'
    elif weekday_number == 3:
        return 'четверг'
    elif weekday_number == 4:
        return 'пятница'
    elif weekday_number == 5:
        return 'суббота'
    elif weekday_number == 6:
        return 'воскресенье'


def get_day_after_tomorrow(date_string):
    # Напишите код функции.
    format = '%Y-%m-%d'
    current_day = dt.strptime(date_string, format)
    week_day = get_weekday_name(current_day.weekday())
    after_tomorrow = get_weekday_name((current_day + td(days=2)).weekday())
    print('Сегодня {0}, {1}, а послезавтра будет {2}'.format(
            date_string, week_day, after_tomorrow))


# Проверьте работу программы, можете подставить свои значения.
get_day_after_tomorrow('2024-01-01')
get_day_after_tomorrow('2024-01-02')
get_day_after_tomorrow('2024-01-03')
get_day_after_tomorrow('2024-01-04')
get_day_after_tomorrow('2024-01-05')
get_day_after_tomorrow('2024-01-06')
