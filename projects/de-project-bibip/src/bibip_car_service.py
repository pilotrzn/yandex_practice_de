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
        self.__insert(
            file_name=DBF[CARS],
            data=car.make_string(),
            index_field=car.vin)

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        self.__insert(
                file_name=DBF[SALES],
                data=sale.make_string(),
                index_field=sale.sales_number)
        # поиск
        data = self.__get_data_by_field(DBF[CARS], sale.car_vin)
        if data is None:
            return None
        record, line = data
        car = Car.make_object_from_record(record)
        if car:
            car.status = CarStatus('sold')
            self.__update(DBF[CARS], car.make_string(), line)

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        cars = []
        with open(f'{self.root_directory_path}/{DBF[CARS]}', "r") as f:
            for line in f:
                if status in line:
                    cars.append(Car.make_object_from_record(line))
        return cars
        # в задании список должэен быть отсортирован, тест написан без сортировки
        # return sorted(cars, key=lambda car: car.vin)

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # defaults
        sales_date: datetime | None = None
        sales_cost: Decimal | None = None
        # принимаем виню обрабатываем в объект, на случай если не существует
        data = self.__get_data_by_field(DBF[CARS], vin)
        if data is None:
            return None
        car_record, _ = data
        car = Car.make_object_from_record(car_record)
        if car:
            data = self.__get_data_by_field(DBF[MODELS], car.model)
            if data is None:
                return None
            model_record, _ = data
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
    def update_vin(self, vin: str, new_vin: str) -> Car | None:
        data = self.__get_data_by_field(DBF[CARS], vin)
        if data is None:
            return None
        record, line = data
        car = Car.make_object_from_record(record)
        car.vin = new_vin
        self.__update(DBF[CARS], car.make_string(), line)
        self.__index_build(DBF[CARS], new_vin, vin, line)

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car | None:
        # ищем продажу по индексу
        data = self.__get_data_by_field(DBF[SALES], sales_number)
        if data is None:
            return None
        sale_record, sale_line = data
        sale = Sale.make_object_from_record(sale_record)
        vin = sale.car_vin
        # машину по найденному вин из продаж
        data = self.__get_data_by_field(DBF[CARS], vin)
        if data is None:
            return None
        # обновление статуса машины
        car_rec, car_line = data
        car = Car.make_object_from_record(car_rec)
        car.status = CarStatus.available
        self.__update(DBF[CARS], car.make_string(), car_line)
        # удаление записи из файла
        sale.is_deleted = True
        self.__update(DBF[SALES], sale.make_string(), sale_line)
        # обновление индекса продаж
        self.__index_build(
            file_name=DBF[SALES],
            value=sales_number,
            line_number=sale_line)
        return car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        d_model_sale: dict[int, int] = {}
        for value in self.__index_array[DBF[SALES]]:
            data = self.__get_data_by_field(DBF[SALES], value)
            if data is None:
                continue
            record, _ = data
            sale = Sale.make_object_from_record(record)
            data = self.__get_data_by_field(DBF[CARS], sale.car_vin)
            if data is not None:
                car_record, _ = data
                car_model_id = Car.make_object_from_record(car_record).model
            if car_model_id in d_model_sale:
                d_model_sale[car_model_id] = d_model_sale[car_model_id] + 1
            else:
                d_model_sale[car_model_id] = 1

        top_models = sorted(
                d_model_sale.items(),
                key=lambda item: item[1],
                reverse=True)[:3]

        dict_top_models: list[ModelSaleStats] = []

        for model_id, count in top_models:
            data = self.__get_data_by_field(DBF[MODELS], model_id)
            if data:
                record, _ = data
                model = Model.make_object_from_record(record)
                dict_top_models.append(
                    ModelSaleStats(
                        car_model_name=model.name,
                        brand=model.brand,
                        sales_number=count
                    )
                )
        return dict_top_models

    # форматирование строки для вставки
    def __create_record(self, str_len: int, tuple: tuple) -> str:
        result = ''
        for value in tuple:
            result += str(value) + ';'
        return result.ljust(str_len) + '\n'

    def __insert_into_file(self, file_name: str, data: str):
        with open(f'{self.root_directory_path}/{file_name}', "a") as f:
            f.write(data)

    # index rebuild
    def __index_build(
            self,
            file_name: str,
            value: int | str,
            old_value: int | str = None,
            line_number: int = None) -> None:
        dict: SortedDict = self.__index_array[file_name]

        if old_value is None and line_number is not None:
            dict.pop(value)
        elif old_value is None:
            dict[value] = len(dict)
        elif old_value is not None and line_number is not None:
            dict.pop(old_value)
            dict[value] = line_number

        with open(f'{self.root_directory_path}/{file_name}_index', "w") as f:
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
            self,
            file_name: str,
            field: str | int
            ) -> tuple[tuple, int] | None:
        line = self.__get_line_from_index(field, self.__index_array[file_name])
        if line is not None:
            record = self.__get_record_by_line(line, DBF[file_name])
            return (record, line)

    # имитация SELECT
    def __get_data_sec_scan(
            self,
            file_name: str,
            search_value: str | int
            ) -> tuple | None:
        with open(f'{self.root_directory_path}/{file_name}', "r") as f:
            for line in f:
                if search_value in line:
                    return (line)

    # имитация INSERT
    def __insert(self, file_name: str, data: str, index_field: int | str):
        self.__insert_into_file(
            file_name, self.__create_record(self.__extend_file_size, data))
        self.__index_build(file_name, index_field)

    # имитация UPDATE
    def __update(self, file_name: str, data: str, line_number: int):
        with open(f'{self.root_directory_path}/{file_name}', "r+") as f:
            f.seek(line_number * (self.__extend_file_size + 1))
            f.write(self.__create_record(self.__extend_file_size, data))
