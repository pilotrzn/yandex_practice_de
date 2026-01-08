import logging

import pendulum
from airflow.decorators import dag, task
from repositories import LedgerLoader

from lib import ConnectionBuilder

log = logging.getLogger(__name__)


WH_CONN = "PG_WAREHOUSE_CONNECTION"

@dag(
    schedule_interval='0 3 * * *',
    start_date=pendulum.datetime(2022, 5, 5, tz="UTC"),
    catchup=False,
    tags=['sprint5', 'cdm', 'project', 'grant5518'],
    is_paused_upon_creation=True
)
def delivery_mart_dag():
    pg_connect = ConnectionBuilder.pg_conn(WH_CONN)

    @task(task_id="load_ledger")
    def load_ledger():
        loader = LedgerLoader(pg_connect, log)
        loader.load()

    # load_restaurants = load_restaurants()
    load_ledger = load_ledger()


delivery_mart_dag = delivery_mart_dag()
