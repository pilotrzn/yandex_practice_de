from datetime import datetime
from logging import Logger
from lib.kafka_connect import KafkaConsumer
from lib.kafka_connect import KafkaProducer
from lib.redis import RedisClient
from stg_loader.repository import StgRepository
from typing import Dict, Any
from pydantic import BaseModel


class Order(BaseModel):
    object_id: int
    object_type: str
    sent_dttm: datetime
    payload: Dict[str, Any]


class StgOrderBuilder:
    def __init__(self, dict: Dict) -> None:
        self._dict = dict

    def get_order_data(self) -> Order:
        return Order(
            object_id=self._dict['object_id'],
            object_type=self._dict['object_type'],
            sent_dttm=self._dict['sent_dttm'],
            payload=self._dict['payload']
        )


class StgMessageProcessor:
    def __init__(self,
                 logger: Logger,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 redis_client: RedisClient,
                 stg_repository: StgRepository,
                 batch_size: int = 100) -> None:
        self._logger = logger
        self._consumer = consumer
        self._producer = producer
        self._redis = redis_client
        self._stg_repository = stg_repository
        self._batch_size = batch_size

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        self._logger.info(f"{datetime.now()}: START")

        for _ in range(self._batch_size):
            msg = self._consumer.consume()
            if not msg or not isinstance(msg, dict):
                self._logger.info(f"{datetime.now()}: No valid message")
                break

            if 'payload' not in msg:
                self._logger.error(f"Invalid message format: {msg}")
                continue

            try:
                builder = StgOrderBuilder(msg)
                order = builder.get_order_data()
                # пишем в пг
                self._stg_repository.order_events_insert(
                    object_id=order.object_id,
                    object_type=order.object_type,
                    sent_dttm=order.sent_dttm,
                    payload=order.payload
                )

                payload = msg['payload']
                user_info = self._redis.get(payload['user']['id'])
                restaurant = self._redis.get(payload['restaurant']['id'])
                order_items = payload['order_items']

                products = []
                menu_dict = {item['_id']: item for item in restaurant['menu']}

                for item in order_items:
                    item_id = item['id']
                    products.append(
                        {
                            'id': item_id,
                            'price': item['price'],
                            'quantity': item['quantity'],
                            'name': menu_dict[item_id]['name'],
                            'category': menu_dict[item_id]['category']
                        }
                    )

                new_msg: Dict[str, Any] = {
                    'object_id':  msg['object_id'],
                    'object_type': msg['object_type'],
                    'payload': {
                        'id': order.object_id,
                        'date': payload['date'],
                        'cost': payload['cost'],
                        'payment': payload['payment'],
                        'status': payload['final_status'],
                        'restaurant': {
                            'id': payload['restaurant']['id'],
                            'name': restaurant['name']
                        },
                        'user': {
                            "id": payload['user']['id'],
                            "name": user_info['name']
                        },
                        'products': products
                    }
                }

                self._producer.produce(new_msg)

            except Exception as e:
                self._logger.error(f"Error processing message: {e}")
                continue
        # Пишем в лог, что джоб успешно завершен.
        self._logger.info(f"{datetime.now()}: FINISH")
