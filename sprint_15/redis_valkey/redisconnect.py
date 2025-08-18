import redis


def main():
# указываем параметры, которые необходимы для подключения
    host = 'c-c9qi5g07kqvo81m63370.rw.mdb.yandexcloud.net'
    port = 6380
    password = 'HLos2Uc2fTFHZkjdpunp'
    ca_path = '/home/aavdonin/.redis/YandexInternalRootCA.crt'

# инициализируем клиент, с помощью которого будем подключаться к Redis
    client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            ssl=True,
            ssl_ca_certs=ca_path)

# просто подключиться недостаточно, да и неинтересно: нужно же ещё и поработать с хранилищем

# запишем в Redis ключ here_is_the_key и соответствующее ему строковое значение string value

    key = "ef8c42c19b7518a9aebec106"
    result = client.get(key)  # Запрашиваем значение ключа

    if not result:
        print("Запись с указанным ключом не найдена.")
        return

    # Декодируем из bytes в строку (Redis возвращает данные в бинарном виде)
    result = result.decode("utf-8")
    print(f"Значение поля 'name' для ключа {key}: {result}")

if __name__ == '__main__':
    main()
