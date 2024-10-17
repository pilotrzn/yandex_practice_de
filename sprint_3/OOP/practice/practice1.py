class Product:
    def __init__(self, product_name: str, remain: int) -> None:
        self.product_name = product_name
        self.remain = remain

    def get_info(self):
        return f'{self.product_name} (в наличии: {self.remain})'


class Kettlebell(Product):
    def __init__(self, product_name: str, remain: int, weight: float) -> None:
        super().__init__(product_name, remain)
        self.weight = weight

    def get_weight(self):
        return f'{self.get_info()}. Вес: {self.weight} кг'


class Clothing(Product):
    def __init__(self, product_name: str, remain: int, size: str) -> None:
        super().__init__(product_name, remain)
        self.size = size

    def get_size(self):
        return f'{self.get_info()}. Размер: {self.size}'


small_kettlebell = Kettlebell('Гиря малая', 15, 2)
shirt = Clothing('Футболка', 5, 'L')
print(small_kettlebell.get_weight())
print(shirt.get_size())
