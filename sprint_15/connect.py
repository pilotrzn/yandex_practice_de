from redis.sentinel import Sentinel

sentinels = [
    'rc1b-ifobd6grccm9djjj.mdb.yandexcloud.net'
]
sentinel = Sentinel([(h, 26379) for h in sentinels], socket_timeout=0.1)
name = "valkey400"
pwd = "HLos2Uc2fTFHZkjdpunp"

master = sentinel.master_for(name, password=pwd)
slave = sentinel.slave_for(name, password=pwd)

master.set("foo", "bar")
print(slave.get("foo"))
