from logging import Logger

from .origin_repository import OriginRepository
from .query_folder import QueryFolder
from models import CourierLedgerObj
from lib import PgConnect
from lib.dict_util import json2str
from psycopg import Connection


class DestRepository:
    def insert(self, conn: Connection, object: CourierLedgerObj,
               query: str) -> None:
        with conn.cursor() as cur:
            cur.execute(
                query,
                {
                    "courier_id": object.courier_id,
                    "courier_name": object.courier_name,
                    "settlement_year": object.settlement_year,
                    "settlement_month": object.settlement_month,
                    "orders_count": object.order_count,
                    "orders_total_sum": object.courier_order_sum,
                    "rate_avg": object.avg_rate,
                    "order_processing_fee": object.order_processing_fee,
                    "courier_order_sum": object.courier_order_sum,
                    "courier_tips_sum": object.courier_tips_sum,
                    "courier_reward_sum": object.courier_reward_sum
                },
            )


class Loader:
# Преобразуем к строке, чтобы положить в БД.
    WF_KEY = "couriers_ledger_workflow"

    def __init__(self, pg_conn: PgConnect, log: Logger) -> None:
        self.pg_dest = pg_conn
        self.origin = OriginRepository[CourierLedgerObj](pg_conn, CourierLedgerObj)
        self.stg = DestRepository()
        self.log = log
        self.sql_dir = QueryFolder()

    def load(self):
        with self.pg_dest.connection() as conn:

            # Вычитываем очередную пачку объектов.
            query = self.sql_dir.load_sql_file("dds_get_ledger.sql")

            load_queue = self.origin.list_all(query)

            self.log.info(f"Found {len(load_queue)} ledgers to load.")
            if not load_queue:
                self.log.info("Quitting.")
                return

            # Сохраняем объекты в базу dwh.
            query = self.sql_dir.load_sql_file("cdm_insert_ledger.sql")
            for object in load_queue:
                self.stg.insert(conn, object, query)
