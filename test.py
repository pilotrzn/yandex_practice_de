from decimal import Decimal, getcontext

getcontext().prec = 3
# Напишите код функции.

def get_monthly_payment(sam, mes, pro):
    res = sam / mes
    resu = (res * pro) / 100
    result = res + resu
    # Функция должна вернуть сумму ежемесячного платежа по кредиту.
    return result


sam = Decimal('54')
mes = Decimal('24')
pro = Decimal('9')
# Вызовите функцию get_monthly_payment() 
# с указанными в задании аргументами
# и распечатайте нужное сообщение.
med = Decimal(str(get_monthly_payment(sam, mes, pro)))
print('Ежемесячный платёж:', med, 'ВтК')



def get_monthly_payment(summ, months, percent):
    # Банк делит названную сумму на названное количество месяцев 
    # и увеличивает ежемесячный платёж на оговоренный процент.
    d_summ = dec(str(summ))
    d_perc = dec(str(percent))
    
    month_pay  = d_summ / months
    month_pay_w_percent = month_pay + month_pay * percent / 100

    # Функция должна вернуть сумму ежемесячного платежа по кредиту.
    return month_pay_w_percent

print ('Ежемесячный платёж:',get_monthly_payment(54, 24, 9) ,'ВтК')  