class Customer:
    def __init__(self, name):
        self.name = name
        self.__discount = 10

    def get_price(self, price: float):
        return round(price * (1 - self.__discount / 100), 2)

    def set_discount(self, discount: float):
        self.__discount = discount if discount < 80 else 80


customer = Customer("Иван Иванович")
customer.get_price(100)
customer.set_discount(20)
customer.get_price(100)
