months = (
    'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 
    'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'
)

for month in months:
    if str.endswith(month,'ь'):
        continue
    print(month)