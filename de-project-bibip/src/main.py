import os
from bibip_car_service import CarService
from models import CarStatus
from raw_data import model_data, car_data, sales_data


root_dir = 'database'


if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    dir_path = f'{os.path.dirname(parent_dir)}/{root_dir}'
    instance = CarService(dir_path)

    for model in model_data():
        instance.add_model(model)

    for car in car_data():
        instance.add_car(car)

    for sale in sales_data():
        instance.sell_car(sale)

    available_cars = instance.get_cars(CarStatus.available)

    car_info = instance.get_car_info("KNAGM4A77D5316538")
    car_info = instance.get_car_info("UPDGM4A77D5316538")
    instance.update_vin("KNAGM4A77D5316538", "UPDGM4A77D5316538")

    removed = instance.revert_sale("20240903#KNAGM4A77D5316538")
    
    top = instance.top_models_by_sales()

    print()
