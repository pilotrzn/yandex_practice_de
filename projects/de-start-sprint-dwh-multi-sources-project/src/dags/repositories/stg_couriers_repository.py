import json
from logging import Logger

from .settings_repository import StgEtlSettingsRepository
from .data_read_repository import DataReader
from .query_folder import QueryFolder
from my_dags.project.models import EtlSetting
from lib import PgConnect
from psycopg import Connection
from lib.dict_util import json2str


class DestRepository:
    def insert(
            self, conn: Connection, object: dict, query: str
            ) -> None:

        with conn.cursor() as cur:
            cur.execute(
                query,
                {
                    "object_id": object["_id"],
                    "object_value": json.dumps(object, ensure_ascii=False)
                },
            )


class Loader:
    WF_KEY = "dlvr_courier_to_stg_workflow"
    LAST_LOADED_ID_KEY = "last_loaded_id"

    def __init__(self,
                 headers: dict,
                 base_url: str,
                 pg_conn: PgConnect,
                 log: Logger) -> None:
        self.pg = pg_conn
        self.log = log
        self.sql_dir = QueryFolder()
        self.setting_repo = StgEtlSettingsRepository(schema="stg")
        self.data_read = DataReader(headers=headers,
                                    url=base_url,
                                    sort_field="id",
                                    log=log)
        self.url = base_url
        self.stg = DestRepository()

    def load(self):
        with self.pg.connection() as conn:
            wf_setting = self.setting_repo.get_setting(conn, self.WF_KEY)
            if not wf_setting:
                # при отсутствии создаем нулевой
                wf_setting = EtlSetting(id=0, workflow_key=self.WF_KEY,
                                        workflow_settings={self.LAST_LOADED_ID_KEY: 0}
                                        )
            full_loaded_objects = []
            offset = wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY]

            query = self.sql_dir.load_sql_file("stg_insert_couriers.sql")
            check = True

            while check:
                loaded_objects = self.data_read.get_data(offset=offset)
                # self.log.info(json.dumps(self.data_read.get_data(offset=offset), ensure_ascii=False))
                
                if not loaded_objects:
                    self.log.info("No data for load. Break cycle.")
                    check = False
                    break

                self.log.info(f"Found {len(loaded_objects)} couriers to load.")
                full_loaded_objects.extend(loaded_objects)
                offset += len(loaded_objects)

            if not full_loaded_objects:
                self.log.info("No data loaded at all. Quitting.")
                return

            for object in full_loaded_objects:
                self.stg.insert(conn, object, query)

            wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY] = offset
            wf_setting_json = json2str(wf_setting.workflow_settings)

            self.setting_repo.save_setting(conn, wf_setting.workflow_key, wf_setting_json)

            self.log.info(f"Load finished on {wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY]}")
