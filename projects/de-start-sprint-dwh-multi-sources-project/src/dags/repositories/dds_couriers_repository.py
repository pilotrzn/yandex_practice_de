from logging import Logger

from .settings_repository import EtlSetting, StgEtlSettingsRepository
from .origin_repository import OriginRepository
from .query_folder import QueryFolder
from models import CourierObj
from lib import PgConnect
from lib.dict_util import json2str
from psycopg import Connection


class DestRepository:
    def insert(self, conn: Connection, object: CourierObj,
               query: str) -> None:
        with conn.cursor() as cur:
            cur.execute(
                query,
                {
                    "courier_id": object.courier_id,
                    "courier_name": object.courier_name
                },
            )


class Loader:
# Преобразуем к строке, чтобы положить в БД.
    WF_KEY = "couriers_stg_to_dds_workflow"
    LAST_LOADED_ID_KEY = "last_loaded_id"
    BATCH_LIMIT = 100

    def __init__(self, pg_conn: PgConnect, log: Logger) -> None:
        self.pg_dest = pg_conn
        self.origin = OriginRepository[CourierObj](pg_conn, CourierObj)
        self.stg = DestRepository()
        self.settings_repository = StgEtlSettingsRepository(schema="dds")
        self.log = log
        self.sql_dir = QueryFolder()

    def load(self):
        with self.pg_dest.connection() as conn:

            wf_setting = self.settings_repository.get_setting(conn, self.WF_KEY)
            if not wf_setting:
                wf_setting = EtlSetting(id=0, workflow_key=self.WF_KEY, workflow_settings={self.LAST_LOADED_ID_KEY: -1})

            # Вычитываем очередную пачку объектов.
            query = self.sql_dir.load_sql_file("stg_get_couriers.sql")

            last_loaded = wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY]
            load_queue = self.origin.list(last_loaded,
                                          self.BATCH_LIMIT, query)
            self.log.info(f"Found {len(load_queue)} couriers to load.")
            if not load_queue:
                self.log.info("Quitting.")
                return

            # Сохраняем объекты в базу dwh.
            query = self.sql_dir.load_sql_file("dds_insert_couriers.sql")
            for object in load_queue:
                self.stg.insert(conn, object, query)

            last_loaded = max([t.id for t in load_queue])
            wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY] = last_loaded
            wf_setting_json = json2str(wf_setting.workflow_settings)
            self.settings_repository.save_setting(conn, wf_setting.workflow_key, wf_setting_json)

            self.log.info(f"Load finished on {wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY]}")
