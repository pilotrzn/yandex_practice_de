from logging import Logger
from airflow.providers.vertica.hooks.vertica import VerticaHook


class StgLoader():
    def __init__(
                self,
                vertica_conn: str,
                schema_name: str,
                dir: str,
                log: Logger):
        self.hook = VerticaHook(vertica_conn_id=vertica_conn)
        self.conn = self.hook.get_conn()
        self.schema = schema_name
        self.data_dir = dir
        self.log = log

    def load_csv_to_vertica(self, file_name: str):

        table_name = f"{file_name.replace('.csv', '')}"
        csv_file = f"{self.data_dir}/{file_name}"
        full_table_name = f"{self.schema}.{table_name}"
        
        cursor = self.conn.cursor()
        try:
            # Очищаем таблицу перед загрузкой
            self.log.info(f"Выполняем TRUNCATE {full_table_name}")
            cursor.execute(f"TRUNCATE TABLE {full_table_name}")
            # Выполняем загрузку через COPY
            copy_command = f"""
                            COPY {full_table_name} 
                            FROM LOCAL '{csv_file}'
                            DELIMITER ','
                            ENCLOSED BY '"'
                            ENFORCELENGTH
                            NO ESCAPE
                            NULL ''
                            SKIP 1
                            REJECTED DATA AS TABLE {full_table_name}_rejected
                        """
            self.log.info("Загружаемся")
            cursor.execute(copy_command)
            self.conn.commit()

        # Проверяем статистику загрузки
            cursor.execute(f"SELECT COUNT(*) FROM {full_table_name}")
            loaded_count = cursor.fetchone()[0]
            self.log.info(f"Successfully loaded {loaded_count} rows into {full_table_name}")

        # Проверяем отброшенные записи
            cursor.execute(f"SELECT COUNT(*) FROM {full_table_name}_rejected")
            rejected_count = cursor.fetchone()[0]
            if rejected_count > 0:
                self.log.info(f"Warning: {rejected_count} rows were rejected")

        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
            self.conn.close()
