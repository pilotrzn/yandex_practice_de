from decimal import Decimal as dec, getcontext

getcontext().prec = 3


# Напишите код функции.
def get_monthly_payment(summ, months, percent):
    # Банк делит названную сумму на названное количество месяцев
    # и увеличивает ежемесячный платёж на оговоренный процент.
    d_summ = dec(str(summ))
    month_pay = d_summ / months
    month_pay_w_percent = month_pay + month_pay * percent / 100

    # Функция должна вернуть сумму ежемесячного платежа по кредиту.
    return month_pay_w_percent


print('Ежемесячный платёж:', get_monthly_payment(54, 24, 9), 'ВтК')
