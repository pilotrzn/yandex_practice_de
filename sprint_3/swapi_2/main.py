from package.save_sw_data import save_sw_data


SWAPI_URL = 'https://swapi.dev/'
SWAPI_MIRROR = 'https://swapi.py4e.com/'


def main():
    try:
        save_sw_data(url=SWAPI_URL)
    except Exception as ex:
        print(f'Ошибка - {ex}')


if __name__ == '__main__':
    main()
