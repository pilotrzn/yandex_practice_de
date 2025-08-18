#!/bin/bash

curl -X POST https://redis-data-service.sprint9.tgcloudenv.ru/load_users \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "c-c9qi5g07kqvo81m63370.rw.mdb.yandexcloud.net",
        "port": "6380",
        "password": "HLos2Uc2fTFHZkjdpunp",
        "ssl": "true",
        "ssl_ca_certs": "/home/aavdonin/git/yandex_practice_de/sprint_15/redis_valkey/YandexInternalRootCA.crt"
        }
}
EOF