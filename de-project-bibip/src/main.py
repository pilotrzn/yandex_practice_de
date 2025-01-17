import os
from bibip_car_service import CarService


root_dir = 'database'


def initialize() -> CarService:
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    dir_path = f'{os.path.dirname(parent_dir)}/{root_dir}'
    create_folder(dir_path=dir_path)
    cs = CarService(dir_path)
    return cs


def create_folder(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


if __name__ == '__main__':
    instance = initialize()
    instance.add_car()
