def get_stickers_comparison(collection_1, collection_2):
    # s_col1 = set(collection_1)
    # s_col2 = set(collection_2)
    s_unique_col1 = set(collection_1) - set(collection_2)
    s_unique_col2 = set(collection_2) - set(collection_1)
    common_col = set(collection_1) & set(collection_2)
    return sorted(s_unique_col1), sorted(s_unique_col2), sorted(common_col)


# Списки стикеров:
stas_collection = ['Тим Бернерс-Ли', 'Линус Торвальдс', 'Ада Лавлейс',
                   'Линус Торвальдс', 'Маргарет Гамильтон', 'Бьярн Страуструп']
anton_collection = ['Тим Бернерс-Ли', 'Гвидо ван Россум', 'Линус Торвальдс',
                    'Бьярн Страуструп', 'Бьярн Страуструп', 'Кен Томпсон',
                    'Деннис Ричи']

# Вызываем функцию и распаковываем полученный кортеж в три переменные:
stas_stickers, anton_stickers, common_stickers = get_stickers_comparison(
    stas_collection, anton_collection)
# Печатаем результаты:

print('Стикеры, которые есть только у Стаса:', stas_stickers)
print('Стикеры, которые есть только у Антона:', anton_stickers)
print('Стикеры, которые есть и у Стаса, и у Антона:', common_stickers)
