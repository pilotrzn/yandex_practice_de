curl -X POST https://valkey-data-service.sprint9.tgcloudenv.ru/test_valkey \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "c-c9qi5g07kqvo81m63370.rw.mdb.yandexcloud.net",
        "port": "6380",
        "password": "HLos2Uc2fTFHZkjdpunp"
    }
}
EOF
