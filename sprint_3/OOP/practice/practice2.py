from datetime import datetime


DATE_FORMAT = '%d.%m.%Y'


class Store:
    weekend = [5, 6]

    def __init__(self, address):
        self.address = address

    def is_open(self, date: datetime):
        return False

    def get_info(self, date_str):
        # С помощью шаблона даты преобразуйте строку date_str в объект даты:
        date_object = datetime.strptime(date_str, DATE_FORMAT)
        if self.is_open(date_object):
            info = 'работает'
        else:
            info = 'не работает'
        return f'Магазин по адресу {self.address} {date_str} {info}'


class MiniStore(Store):
    def is_open(self, date):
        return False if date.weekday() in self.weekend else True


class WeekendStore(Store):
    def is_open(self, date):
        return True if date.weekday() in self.weekend else False


class NonStopStore(Store):
    def is_open(self, date):
        return True


mini_store = MiniStore('Улица Немига, 57')
print(mini_store.get_info('29.03.2024'))
print(mini_store.get_info('30.03.2024'))

weekend_store = WeekendStore('Улица Толе би, 321')
print(weekend_store.get_info('29.03.2024'))
print(weekend_store.get_info('30.03.2024'))

non_stop_store = NonStopStore('Улица Арбат, 60')
print(non_stop_store.get_info('29.03.2024'))
print(non_stop_store.get_info('30.03.2024'))
