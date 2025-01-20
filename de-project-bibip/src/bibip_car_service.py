import os
import shutil
from datetime import datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from sortedcontainers import SortedDict


CARS = "cars"
MODELS = "models"
SALES = "sales"

DBF = {
    CARS: "cars",
    MODELS: "models",
    SALES: "sales"
}


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.__extend_file_size = 500
        self.__extend_index_size = 20
        self.__index_array = {}
        # создание каталога бд
        if os.path.exists(self.root_directory_path):
            shutil.rmtree(self.root_directory_path)
        os.makedirs(self.root_directory_path, exist_ok=True)
        # создание файлов бд
        for file in DBF:
            open(f'{self.root_directory_path}/{DBF[file]}', "a").close()
            open(f'{self.root_directory_path}/{DBF[file]}_index', "a").close()
        # словарь с отсортированными индексами
        for name in DBF:
            self.__index_array[name] = SortedDict()

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model):
        self.__insert(
            file_name=DBF[MODELS],
            data=model.make_string(),
            index_field=model.id)

    def add_car(self, car: Car):
        self.__insert(DBF[CARS], car.make_string(), car.vin)

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        self.__insert(
                DBF[SALES], sale.make_string(), sale.sales_number)
        # поиск
        current_record, line = self.__get_data_by_field(
                                                DBF[CARS], sale.car_vin)
        current_car = Car.make_object_from_record(current_record)
        if current_car:
            current_car.status = CarStatus('sold')
            self.__update(DBF[CARS], current_car.make_string(), line)

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        cars = []
        with open(f'{self.root_directory_path}/{DBF[CARS]}', "r") as f:
            for line in f:
                if status in line:
                    cars.append(Car.make_object_from_record(line))
        return sorted(cars, key=lambda car: car.vin)

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        sales_date: datetime | None = None
        sales_cost: Decimal | None = None
        # принимаем вин
        car_record, _ = self.__get_data_by_field(DBF[CARS], vin)
        car = Car.make_object_from_record(car_record)
        if car:
            model_record, _ = self.__get_data_by_field(
                DBF[MODELS], car.model)
            model = Model.make_object_from_record(model_record)
        # если статус машины продана-ищем данные о продаже
        if car.status == CarStatus.sold:
            sale_record = self.__get_data_sec_scan(DBF[SALES], vin)
            sale = Sale.make_object_from_record(sale_record)
            if sale:
                sales_date = sale.sales_date
                sales_cost = sale.cost

        return CarFullInfo(
            vin=vin,
            car_model_name=model.name,
            car_model_brand=model.brand,
            price=car.price,
            date_start=car.date_start,
            status=car.status,
            sales_date=sales_date,
            sales_cost=sales_cost
        )

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        record, line = self.__get_data_by_field(DBF[CARS], vin)
        car = Car.make_object_from_record(record)
        car.vin = new_vin

        self.__update(DBF[CARS], car.make_string(), line)
        # придумать
        self.__index_update(DBF[CARS], line, vin, new_vin)

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError

    # форматироввание строки для вставки
    def __create_record(self, str_len: int, tuple: tuple) -> str:
        result = ''
        for value in tuple:
            result += str(value) + ';'
        return result.ljust(str_len) + '\n'

    def __insert_into_file(self, file_name: str, data: str):
        with open(f'{self.root_directory_path}/{file_name}', "a") as f:
            f.write(data)

    # index rebuild
    def __insert_into_index(self, file_name: str, element: int | str) -> None:
        dict = self.__index_array[file_name]
        with open(f'{self.root_directory_path}/{file_name}_index', "w") as f:
            dict[element] = len(dict)
            arr = []
            for i in dict.items():
                str = self.__create_record(
                    self.__extend_index_size, (i[0], i[1]))
                arr.append(str)
            f.writelines(arr)

    def __get_line_from_index(
            self, value: str | int, index: SortedDict) -> int | None:
        return index[value] if value in index else None

    def __get_record_by_line(
            self, line_number: int, file_name: str) -> str | None:
        with open(f'{self.root_directory_path}/{file_name}', "r") as f:
            f.seek(line_number * (self.__extend_file_size + 1))
            return f.read(self.__extend_file_size)

    def __get_data_by_field(
            self, file_name: str, field: str | int) -> tuple[tuple, int]:
        line = self.__get_line_from_index(field, self.__index_array[file_name])
        if line is not None:
            record = self.__get_record_by_line(line, DBF[file_name])
            return (record, line)

    # имитация SELECT
    def __get_data_sec_scan(
            self, file_name: str, search_value: str | int) -> tuple | None:
        with open(f'{self.root_directory_path}/{file_name}', "r") as f:
            for line in f:
                if search_value in line:
                    return (line)

    # имитация INSERT
    def __insert(self, file_name: str, data: str, index_field: int | str):
        self.__insert_into_file(
            file_name, self.__create_record(self.__extend_file_size, data))
        self.__insert_into_index(file_name, index_field)

    # имитация UPDATE
    def __update(self, file_name: str, data: str, line_number: int):
        with open(f'{self.root_directory_path}/{file_name}', "r+") as f:
            f.seek(line_number * (self.__extend_file_size + 1))
            f.write(self.__create_record(self.__extend_file_size, data))

    def __index_update(
                self,
                file_name: str,
                line_number: int,
                old_val: int | str,
                new_val: int | str):
        with open(f'{self.root_directory_path}/{file_name}_index', "r+") as f:
            f.seek(line_number * (self.__extend_index_size + 1))
            f.write(self.__create_record(self.__extend_index_size, new_val))
        self.__index_array[file_name].pop(old_val)
        self.__insert_into_index(file_name, new_val)
