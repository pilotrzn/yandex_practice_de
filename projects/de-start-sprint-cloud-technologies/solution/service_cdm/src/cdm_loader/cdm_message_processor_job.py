from datetime import datetime
from logging import Logger
from lib.kafka_connect import KafkaConsumer
from cdm_loader.repository import Loader, DbInsert


class CdmMessageProcessor:
    def __init__(
            self,
            logger: Logger,
            consumer: KafkaConsumer,
            db_insert: DbInsert,
            batch_size: int = 100) -> None:

        self._consumer = consumer
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
                loader = Loader(msg['payload'], 'kafka-dds-service-orders')

                # вставки в таблицы бд
                self._db_insert.user_cat_insert(loader.user_category_counters())
                self._db_insert.user_prod_insert(loader.user_product_counters())

            except Exception as e:
                self._logger.error(f"Error processing message: {e}")
                continue
        # Пишем в лог, что джоб успешно завершен.
        self._logger.info(f"{datetime.now()}: FINISH")
