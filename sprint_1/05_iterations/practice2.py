def count_canisters(temperatures_per_day):
    hot_days_counter = 0
    for temp in temperatures_per_day:
        if temp >= 30: 
            hot_days_counter+= 1 
    return(hot_days_counter)

forecast_temperatures = [26, 28, 30, 31, 29, 31, 28, 26]

print(f'Нужно канистр: {count_canisters(forecast_temperatures)}')