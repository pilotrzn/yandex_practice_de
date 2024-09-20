# Получаем данные в секундах
response = 424562

# Переведите полученное значение в необходимые единицы измерения
days = response // (24 * 60 * 60)
hours = response // (60 * 60) % 24
minutes = response // 60 % 60
seconds = 424562 % 60

print(response, 'секунд - это')
print('Дней:', days)
print('Часов:', hours)
print('Минут:', minutes)
print('Секунд:', seconds)