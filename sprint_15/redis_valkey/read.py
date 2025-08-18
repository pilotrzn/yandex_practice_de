import json
from typing import Dict
import redis


order_items = [
            {
                "id": "30ec47e5baea70b664df6bff",
                "name": "\u041f\u043b\u043e\u0432 \u0444\u0435\u0440\u0433\u0430\u043d\u0441\u043a\u0438\u0439",
                "price": 420,
                "quantity": 4
            },
            {
                "id": "bfdf489791e9bc1eb3eefbf5",
                "name": "\u041b\u0430\u0433\u043c\u0430\u043d",
                "price": 350,
                "quantity": 2
            }
        ]


class RedisClient:
    def __init__(
            self,
            host: str,
            port: int,
            password: str,
            cert_path: str
    ) -> None:
        self._client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            ssl=True,
            ssl_ca_certs=cert_path,
            decode_responses=True)

    def set(self, k: str, v: Dict):
        self._client.set(k, json.dumps(v))

    def get(self, k: str) -> Dict:
        result = self._client.get(k)
        return json.loads(result)


if __name__ == '__main__':
    rc = RedisClient(
        host="c-c9qi5g07kqvo81m63370.rw.mdb.yandexcloud.net",
        port=6380,
        password="HLos2Uc2fTFHZkjdpunp",
        cert_path="/home/aavdonin/git/yandex_practice_de/sprint_15/redis_valkey/YandexInternalRootCA.crt"
        )
    restaurant = rc.get('ebfa4c9b8dadfc1da37ab58d')
    user = rc.get('626a81ce9a8cd1920641e284')
    menu = restaurant['menu']
    print(f'user: {user['name']}')
    print(f'rest: {restaurant['name']}')
    menu_dict = {item['_id']: item for item in menu}
    print(menu_dict)


    for ord in order_items:
        if ord['id'] in menu_dict:
            
            print(ord)
    
    # for product in products:
        # print(str(product))
