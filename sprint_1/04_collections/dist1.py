
def create_vegetable_info(vegetables, varieties, yields):
    # Ваш код здесь
    # z_var_yi = zip(varieties,yields)
    z_veg_zip = zip(vegetables, zip(varieties, yields))
    vegetable_info = dict(z_veg_zip)
    return vegetable_info


# Тестовые данные:
vegetables = ['Помидоры', 'Огурцы', 'Баклажаны', 'Перец', 'Капуста']
varieties = ['Красный куб', 'Аллигатор', 'Василёк', 'Тропический закат', 'Арктик']
yields = [6.5, 4.3, 2.8, 2.2, 3.5]

# Вызов функции:
print(create_vegetable_info(vegetables, varieties, yields))