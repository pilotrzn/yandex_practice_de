import os
import shutil


REPORT_CAT = '/data'
EXTENSION = '.txt'


def create_folder(dir_path: str):
    shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)


def create_file(file_name: str, request_text: str):
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    # Получаем путь до родительского каталога проекта
    # чтобы не создавать в текущем каталоге
    dir_path = f'{os.path.dirname(parent_dir)}{REPORT_CAT}'
    # create_folder(dir_path=dir_path)
    file_path = f'{dir_path}/{file_name}{EXTENSION}'
    with open(file_path, 'w', encoding='utf-8') as result_file:
        result_file.write(request_text)
