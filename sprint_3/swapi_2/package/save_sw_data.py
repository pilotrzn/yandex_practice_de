import os
import shutil
from package.cls_swrequester import SWRequester


REPORT_CAT = 'data'
EXTENSION = '.txt'


def save_sw_data(url: str):
    try:
        # Получаем путь до родительского каталога проекта
        # чтобы не создавать в текущем каталоге
        parent_dir = os.path.dirname(os.path.realpath(__file__))
        dir_path = f'{os.path.dirname(parent_dir)}/{REPORT_CAT}'
        create_folder(dir_path=dir_path)
        swapi_instance = SWRequester()
        swapi_instance.set_url(url=url)
        categories = swapi_instance.get_sw_categories()
        for category in categories:
            file_path = f'{dir_path}/{category}{EXTENSION}'
            cat_info = swapi_instance.get_sw_info(categories[category])
            create_file(file_name=file_path, request_text=cat_info)
    except Exception as ex:
        print(f'Ошибка - {ex}')


def create_folder(dir_path: str):
    shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)


def create_file(file_name: str, request_text: str):
    with open(file_name, 'w', encoding='utf-8') as result_file:
        result_file.write(request_text)
