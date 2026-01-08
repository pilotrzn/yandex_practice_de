import time
import requests
import psycopg2

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.providers.postgres.hooks.postgres import PostgresHook

postgres_conn_id = 'pg_connection'

args = {
    "owner": "student",
    'email': ['student@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

business_dt = '{{ ds }}'

with DAG(
        'customer_retention_weekly',
        default_args=args,
        catchup=True,
        start_date=datetime.today() - timedelta(weeks=6),
        schedule_interval='0 3 * * 1',
) as dag:

    customer_retention_update = PostgresOperator(
        task_id = 'mart_customer_retention_update',
        postgres_conn_id=postgres_conn_id,
        sql = "sql/mart.f_customer_retention.sql")

customer_retention_update