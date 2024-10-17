import requests

url = 'http://wttr.in/?0T'

response = requests.get(url)  # Выполните HTTP-запрос.

print(response.text)  # Напечатайте статус-код ответа.

search_parameters = {
    'text': 'кто такой инженер данных',
    'lr': 213
}
url = 'https://yandex.ru/search/'
# Функция get() приняла на вход URL и параметры поиска,
# а дальше она знает, что делать.
response = requests.get(url, params=search_parameters)

print(response.status_code)
print(response.url)