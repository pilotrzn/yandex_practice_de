from typing import Optional

from psycopg import Connection
from psycopg.rows import class_row
from my_dags.project.models import EtlSetting
from .query_folder import QueryFolder


class StgEtlSettingsRepository:
    def __init__(self, schema):
        self.sql_dir = QueryFolder()
        self.schema = schema

    def get_setting(self,
                    conn: Connection,
                    etl_key: str) -> Optional[EtlSetting]:

        query = self.sql_dir.load_sql_file(f"{self.schema}_get_settings.sql")

        with conn.cursor(row_factory=class_row(EtlSetting)) as cur:
            cur.execute(
                query,
                {"etl_key": etl_key},
            )
            obj = cur.fetchone()
        return obj

    def save_setting(self, conn: Connection,
                     workflow_key: str, workflow_settings: str) -> None:

        query = self.sql_dir.load_sql_file(f"{self.schema}_insert_settings.sql")
        with conn.cursor() as cur:
            cur.execute(
                query,
                {
                    "etl_key": workflow_key,
                    "etl_setting": workflow_settings
                },
            )