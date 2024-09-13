vegetables = ['Помидоры', 'Огурцы', 'Баклажаны', 'Перец', 'Капуста']
vegetable_yields = [6.5, 4.3, 2.8, 2.2, 3.5]

for index in range(len(vegetable_yields)):
    str = f'{vegetables[index]}: урожайность - {vegetable_yields[index] *  10000:.0f} кг на гектар.'
    print(str)



vegetables = ['Помидоры', 'Огурцы', 'Баклажаны', 'Перец'] # Этот список короче.
vegetable_yields = [6.5, 4.3, 2.8, 2.2, 3.5]

for i in range(len(vegetable_yields)):
    if i < len(vegetables):
        print(f'{vegetables[i]}: урожайность - {vegetable_yields[i] * 10000:.0f} кг на гектар.')