from decimal import Decimal , getcontext
getcontext().prec = 3

def assess_yield(number_of_plants, average_weight):
    # Ваш код здесь
    d_av_weight = Decimal(str(average_weight))
    full_weight = d_av_weight * number_of_plants / 1000
    mes = ''

    if full_weight > 100:
        mes = 'Ожидается отличный урожай.'
    elif 50 <= full_weight <= 100:
        mes = 'Ожидается хороший урожай.'
    elif 0 < full_weight < 50:
        mes = 'Урожай будет так себе.'
    else:
        mes = 'Урожая не будет.'
    return float(full_weight), mes

# Пример вызова функции
total_weight, rating = assess_yield(100, 100)
print(total_weight, 'кг.', rating)