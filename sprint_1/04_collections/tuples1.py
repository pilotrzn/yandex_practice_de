from decimal import Decimal , getcontext
getcontext().prec = 3

def assess_yield(number_of_plants, average_weight):
    # Ваш код здесь
    d_av_weight = Decimal(str(average_weight)) / 1000
    full_weight = float(d_av_weight * number_of_plants) 
    mes = ''
    print(d_av_weight,full_weight)
    
    if full_weight > 100:
        mes = 'Ожидается отличный урожай.'
    elif 50 <= full_weight <= 100:
        mes = 'Ожидается хороший урожай.'
    elif 0 < full_weight < 50:
        mes = 'Урожай будет так себе.'
    else:
        mes = 'Урожая не будет.'

    print(full_weight)
    return float(full_weight), mes

# Пример вызова функции
total_weight, rating = assess_yield(101, 500)
print(total_weight, 'кг.', rating)