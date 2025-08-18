#!/bin/bash


curl -X POST https://rc1b-ifobd6grccm9djjj.mdb.yandexcloud.net/test_valkey \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "valkey":{
        "host": "c-c9qi5g07kqvo81m63370.rw.mdb.yandexcloud.net",
        "port": 6380,
        "password": "HLos2Uc2fTFHZkjdpunp",
        "ssl": true,
        "ssl_ca_certs": "/home/aavdonin/.redis/YandexInternalRootCA.crt"
    }
}
EOF


curl -X POST https://redis-data-service.sprint9.tgcloudenv.ru/load_users \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "c-c9qi5g07kqvo81m63370.rw.mdb.yandexcloud.net",
        "port": 6380,
        "password": "HLos2Uc2fTFHZkjdpunp"
}
EOF