from datetime import datetime
from logging import Logger
from lib.kafka_connect import KafkaConsumer, KafkaProducer
from dds_loader.repository import Loader, DbInsert


class DdsMessageProcessor:
    def __init__(
            self,
            logger: Logger,
            consumer: KafkaConsumer,
            producer: KafkaProducer,
            db_insert: DbInsert,
            batch_size: int = 100) -> None:

        self._consumer = consumer
        self._producer = producer
        self._db_insert = db_insert
        self._logger = logger
        self._batch_size = batch_size

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
                loader = Loader(msg['payload'], 'kafka-stg-service-orders')

                # вставки в таблицы бд Хабы
                self._db_insert.hub_user_insert(loader.hub_user())
                self._db_insert.hub_order_insert(loader.hub_order())
                self._db_insert.hub_restaurant_insert(loader.hub_restaurant())
                self._db_insert.hub_product_insert(loader.hub_product())
                self._db_insert.hub_category_insert(loader.hub_category())

                # вставки в бд Линки
                self._db_insert.link_order_product_insert(loader.link_order_product())
                self._db_insert.link_order_user_insert(loader.link_order_user())
                self._db_insert.link_prod_category_insert(loader.link_product_category())
                self._db_insert.link_prod_rest_insert(loader.link_product_restaurant())

                # вставки в таблицы бд Сателлиты

                self._db_insert.sat_order_status_insert(loader.sat_order_status())
                self._db_insert.sat_product_names_insert(loader.sat_product_names())
                self._db_insert.sat_restaurant_names_insert(loader.sat_restaurant_names())
                self._db_insert.sat_user_names_insert(loader.sat_user_names())
                self._db_insert.sat_order_cost_insert(loader.sat_order_cost())

                self._producer.produce(loader.gen_output_message())

            except Exception as e:
                self._logger.error(f"Error processing message: {e}")
                continue
        # Пишем в лог, что джоб успешно завершен.
        self._logger.info(f"{datetime.now()}: FINISH")
