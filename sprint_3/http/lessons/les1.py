import urllib.parse


user_query = 'Как стать инженером данных'
url = 'https://yandex.ru/search/?text=' + '%20'.join(user_query.split(' '))
print(url)

strings = [
    'кто такой инженер данных',
    'Привет!',
    ' ',        # Просто пробел.
    'letiště',  # Аэропорт по-чешски.
    'München',  # Крупнейший город Баварии.
    'Champs-Élysées',  # Елисейские поля.
    '東京',     # А это Токио.
]
for s in strings:
    encoded = urllib.parse.quote(s)          # Зашифрованная строка.
    decoded = urllib.parse.unquote(encoded)  # Расшифрованная обратно строка.
    print(decoded, '-', encoded)


url = 'https://yandex.ru/search/?text=%D0%BA%D0%B0%D0%BA%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%20%D0%B5%D0%B7%D0%B4%D0%B8%D1%82%D1%8C%20%D0%BD%D0%B0%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8'

question = url.split('=')[1]
print(urllib.parse.unquote(question))
