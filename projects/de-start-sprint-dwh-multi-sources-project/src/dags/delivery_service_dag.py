import logging

import pendulum
from airflow.decorators import dag, task
from repositories import (
    CourierLoaderStg,
    DeliveryLoaderStg,
    CourierLoader,
    TsLoader,
    DeliveryLoader,
    FactDeliveryLoader
    )

from lib import ConnectionBuilder

log = logging.getLogger(__name__)


NICKNAME = "grant5518"
COHORT = "4"
BASE_URL = "https://d5d04q7d963eapoepsqr.apigw.yandexcloud.net"
API_KEY = "25c27781-8fde-4b30-a22e-524044a7580f"
WH_CONN = "PG_WAREHOUSE_CONNECTION"


@dag(
    schedule_interval='0/25 * * * *',
    start_date=pendulum.datetime(2022, 5, 5, tz="UTC"),
    catchup=False,
    tags=['sprint5', 'stg', 'project', 'grant5518'],
    is_paused_upon_creation=True
)
def delivery_service_dag():
    pg_connect = ConnectionBuilder.pg_conn(WH_CONN)
    headers = {
        "X-Nickname": NICKNAME,
        "X-Cohort": COHORT,
        "X-API-KEY": API_KEY
    }

    @task(task_id="load_couriers_stg")
    def load_couriers_stg():
        url = f"{BASE_URL}/couriers"
        loader = CourierLoaderStg(headers, url, pg_connect, log)
        loader.load()

    @task(task_id="load_deliveries_stg")
    def load_deliveries_stg():
        url = f"{BASE_URL}/deliveries"
        loader = DeliveryLoaderStg(headers, url, pg_connect, log)
        loader.load()

    @task(task_id="load_couriers_dds")
    def load_couriers_dds():
        loader = CourierLoader(pg_connect, log)
        loader.load()

    @task(task_id="load_dlvr_timestamps_dds")
    def load_timestamps():
        loader = TsLoader(pg_connect, log)
        loader.load()

    @task(task_id="load_deliveries_dds")
    def load_deliveries():
        loader = DeliveryLoader(pg_connect, log)
        loader.load()

    @task(task_id="load_facts_dds")
    def load_facts():
        loader = FactDeliveryLoader(pg_connect, log)
        loader.load()

    # load_restaurants = load_restaurants()
    load_couriers_stg = load_couriers_stg()
    load_deliveries_stg = load_deliveries_stg()
    load_couriers_dds = load_couriers_dds()
    load_timestamps = load_timestamps()
    load_deliveries = load_deliveries()
    load_facts = load_facts()

    (
        [load_couriers_stg, load_deliveries_stg]
        >> load_couriers_dds
        >> load_timestamps
        >> load_deliveries
        >> load_facts
    )


delivery_service_dag = delivery_service_dag()
