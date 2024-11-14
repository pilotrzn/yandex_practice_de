cards = [
    {
        'number': 2,
        'color': 'Белый'
    },
    {
        'number': 9,
        'color': 'Серо-голубой'
    },
    {
        'number': 11,
        'color': 'Коралловый'
    },
    {
        'number': 7,
        'color': 'Зелёный'
    },
    {
        'number': 1,
        'color': 'Чёрный'
    },
]

result = sorted(cards, key=lambda item: item['color'])
print(result)