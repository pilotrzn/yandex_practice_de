# Пригодится для наполнения списков!
import random


harvest = [[random.randint(5,20) for _ in range(3)] for _ in range(3)]  

def total_harvest(_harvest):
    summ = 0
    for harv in _harvest:
        summ += sum(harv)
    return summ

def average_harvest_per_plot(_harvest):
    return [ sum(harv) / len(harv) for harv in _harvest ]

    
print('Урожай с каждой грядки на каждом участке:', harvest)
print('Общий урожай со всех участков:', total_harvest(harvest))
print('Средний урожай с каждого участка:', average_harvest_per_plot(harvest))
