import redis

r = redis.StrictRedis(
    host="c-c9qi5g07kqvo81m63370.rw.mdb.yandexcloud.net",
    port=6380,
    password="HLos2Uc2fTFHZkjdpunp",
    ssl=True,
    ssl_ca_certs="/home/aavdonin/.redis/YandexInternalRootCA.crt",
)

r.set("foo", "bar")
print(r.get("foo"))
