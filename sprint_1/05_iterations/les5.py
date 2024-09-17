fruit_yields = [164.8, 105.0, 124.3, 113.8]  # Урожайность, кг на дерево.

# for yield_value in fruit_yields:
#     yield_value += 1.2
#     list.append(corrected_fruit_yields, yield_value)

corrected_fruit_yields = [ value + 1.2 for value in fruit_yields ]  # Ваш код - здесь.

print(corrected_fruit_yields)


numbers = [] 

numbers =[value ** 2 for value in range(1,11)]# Место для вашего кода
print(numbers)