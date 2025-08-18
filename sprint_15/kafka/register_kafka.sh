curl -X POST https://order-gen-service.sprint9.tgcloudenv.ru/register_kafka \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "student": "grant5518",
    "kafka_connect":{
        "host": "rc1b-lsg5qa80e53hscub.mdb.yandexcloud.net",
        "port": 9091,
        "topic": "order-service_orders",
        "producer_name": "producer_consumer",
        "producer_password": "2xY5fjrpenZkgMwomS2H"
    }
}
EOF