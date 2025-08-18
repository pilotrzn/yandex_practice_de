from confluent_kafka import Producer

def error_callback(err):
    print('Something went wrong: {}'.format(err))

params = {
    'bootstrap.servers': 'rc1b-lsg5qa80e53hscub.mdb.yandexcloud.net:9091',
    'security.protocol': 'SASL_SSL',
    'ssl.ca.location': '/home/aavdonin/git/yandex_practice_de/sprint_15/kafka/YandexInternalRootCA.crt',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': 'producer_consumer',
    'sasl.password': '2xY5fjrpenZkgMwomS2H',
    'error_cb': error_callback,
}

p = Producer(params)
p.produce('order-service_orders', 'some payload1')
p.flush(10)
