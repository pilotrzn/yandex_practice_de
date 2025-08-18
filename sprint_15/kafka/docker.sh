docker run \
    -it \
    --network=host \
    -v /home/aavdonin/git/yandex_practice_de/sprint_15/kafka/YandexInternalRootCA.crt:/data/YandexInternalRootCA.crt \
    edenhill/kcat:1.7.1 -b rc1b-lsg5qa80e53hscub.mdb.yandexcloud.net:9091 \
    -X security.protocol=SASL_SSL \
    -X sasl.mechanisms=SCRAM-SHA-512 \
    -X sasl.username=producer_consumer \
    -X sasl.password=2xY5fjrpenZkgMwomS2H \
    -X ssl.ca.location=/data/YandexInternalRootCA.crt \
    -L 



docker run \
    -it \
    --name "kcat" \
    --network=host \
    --rm \
    -v /home/aavdonin/git/yandex_practice_de/sprint_15/kafka/YandexInternalRootCA.crt:/data/YandexInternalRootCA.crt  \
    edenhill/kcat:1.7.1 -b rc1b-lsg5qa80e53hscub.mdb.yandexcloud.net:9091 \
    -X security.protocol=SASL_SSL \
    -X sasl.mechanisms=SCRAM-SHA-512 \
    -X sasl.username=producer_consumer \
    -X sasl.password=2xY5fjrpenZkgMwomS2H \
    -X ssl.ca.location=/data/YandexInternalRootCA.crt \
    -t order-service_orders \
    -C \
    -o beginning 