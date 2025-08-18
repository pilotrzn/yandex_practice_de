from confluent_kafka import Consumer
import json


def error_callback(err):
    print('Something went wrong: {}'.format(err))


params = {
    'bootstrap.servers': 'rc1b-lsg5qa80e53hscub.mdb.yandexcloud.net:9091',
    'security.protocol': 'SASL_SSL',
    'ssl.ca.location': '/home/aavdonin/git/yandex_practice_de/sprint_15/kafka/YandexInternalRootCA.crt',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': 'producer_consumer',
    'sasl.password': '2xY5fjrpenZkgMwomS2H',
    'group.id': 'main-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
    'error_cb': error_callback,
    'debug': 'all',
}

c = Consumer(params)
c.subscribe(['stg-service-orders'])
# while True:
#     for i in range(12):
#         print(f'round {i}')
#         msg = c.poll(timeout=3.0)
#         if not msg:
#             break

#         if msg:
#             val = msg.value().decode()
#             with open('results', "a") as f:
#                 f.write(val)
#             print(val)

with open('stg-service-orders.json', 'a') as f:
    while True:
        f.write('\n')
        for i in range(12):
            print(f'round {i}')
            msg = c.poll(timeout=3.0)
            if not msg:
                break

            if msg:
                try:
                    val = msg.value().decode('utf-8')
                    # Парсим как JSON
                    json_data = json.loads(val)
                    # Декодируем сообщение
                    # Записываем как JSON с новой строки
                    json.dump(json_data, f, ensure_ascii=False)
                    f.write('\n')  # Добавляем перенос строки
                    f.flush()  # Обеспечиваем запись на диск
                except json.JSONDecodeError as e:
                    print(f'Invalid JSON: {val}, error: {e}')
                except UnicodeDecodeError as e:
                    print(f'Decoding error: {e}')
