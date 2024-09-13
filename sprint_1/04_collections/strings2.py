# Количество корзин с овощами, шт.
baskets = 462 
# Средний вес овощей в одной корзине, кг.
average_weight = 25
# Стоимость одного килограмма урожая, в монетах.
price_per_kg = 175 


# Допишите функцию, которая рассчитывает вес и стоимость урожая.
def calc(basket_count, average_weight, price_per_kg):
    weight = basket_count * average_weight
    full_price = weight * price_per_kg

    return weight, full_price
# Вызовите функцию calc() и обработайте вернувшееся значение.

weight, full_price = calc(basket_count=baskets, price_per_kg=price_per_kg, average_weight=average_weight)


print(f'Общий вес урожая: {weight} кг. Оценённая стоимость урожая: {full_price}.')