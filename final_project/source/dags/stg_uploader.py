import logging
import os
import sys
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.vertica.hooks.vertica import VerticaHook

log = logging.getLogger(__name__)


def upload_data(
        pg_conn_id: str,
        vertica_conn_id: str,
        table_name: str,
        dt_column: str,
        path_to_csv: str = '/data'):
    log.info(f'Load and insert into {table_name}')

    vert_conn = VerticaHook(vertica_conn_id).get_conn()
    pg_conn = PostgresHook(pg_conn_id).get_conn()

    try:
        vert_cur = vert_conn.cursor()
        sql = f"""
                SELECT coalesce(max({dt_column}), '1900-01-01 00:00:00')
                FROM STV202504297__STAGING.{table_name};
            """
        vert_cur.execute(sql)
        last_datetime = vert_cur.fetchone()[0]

        log.info(f"Last record dt STV202504297__STAGING.{table_name} = {last_datetime}")

    except Exception as e:
        log.info("Error:", e)
        sys.exit()

    log.info("Load to CSV begin...")

    try:
        pg_sql = f"SELECT * FROM public.{table_name} WHERE {dt_column} > '{last_datetime}';"
        df = pd.read_sql(pg_sql, pg_conn)

        if df.shape[0] == 0:
            log.info("No data.")
            return
        else:
            with open(f"{path_to_csv}/{table_name}.csv", "w") as file:
                df.to_csv(file, index=False)
            log.info(f"{table_name} export to csv...")

    except Exception as e:
        log.info("Error:", e)
        sys.exit()

    log.info(f"Load to STV202504297__STAGING.{table_name} from CSV...")

    try:
        sql_columns = str(tuple(df.columns)).replace("'", "")
        vert_sql = f"""
                COPY STV202504297__STAGING.{table_name}{sql_columns}
                FROM LOCAL '{path_to_csv}/{table_name}.csv'
                DELIMITER ','
                REJECTED DATA AS TABLE STV202504297__STAGING.{table_name}_rej;
            """
        vert_cur.execute(vert_sql)
        log.info(f"STV202504297__STAGING.{table_name} loaded from csv.")
        os.remove(f'{path_to_csv}/{table_name}.csv')

    except Exception as e:
        log.info("Error:", e)
        sys.exit()
