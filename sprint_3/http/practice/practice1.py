import os
import requests


cities = [
    'Омск',
    'Калининград',
    'Челябинск',
    'Владивосток',
    'Красноярск',
    'Москва',
    'Екатеринбург'
]


def make_url(city):
    # в URL задаём город, в котором узнаем погоду
    return f'http://wttr.in/{city}'


def make_parameters():
    params = {
        'format': 2,  # погода одной строкой
        'M': '',      # скорость ветра в "м/с"
        'T': ''       # передать символы в упрощённом виде
    }
    return params


def what_weather(city):
    url = make_url(city)
    weather_parameters = make_parameters()
    try:
        response = requests.get(url, params=weather_parameters)
        response.raise_for_status()
    except requests.ConnectionError:
        return '<ошибка на сервере погоды>'
    return response.text


dir_path = os.path.dirname(os.path.realpath(__file__)) + '/data'
os.makedirs(dir_path, exist_ok=True)

for city in cities:
    weather_report = what_weather(city)
    file_path = f'{dir_path}/{city}.txt'
    with open(file_path, 'w', encoding='utf-8') as result_file:
        result_file.write(weather_report)
