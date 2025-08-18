from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import pendulum
import logging

from stg_uploader import upload_data


log = logging.getLogger(__name__)

# подключения в airflow
pg_conn_id = 'pg_conn'
vertica_conn_id = 'vertica_conn'

args = {
    "owner": "grant5518",
    'retries': 3
}

with DAG(
    dag_id='upload_data',
    default_args=args,
    schedule_interval='@daily',
    start_date=pendulum.parse('2022-10-01'),
    end_date=pendulum.parse('2022-11-02'),
    catchup=True,
    tags=['final_project', 'upload_data', 'postgres_to_stg', 'postgres']
) as dag:

    staging_ddl = SQLExecuteQueryOperator(
        task_id='staging_ddl',
        conn_id=vertica_conn_id,
        database='Vertica',
        sql='sql/ddl_vertica_staging.sql'
    )

    load_currencies = PythonOperator(
        task_id='load_currencies',
        python_callable=upload_data,
        op_kwargs={'table_name': 'currencies',
                   'dt_column': 'date_update',
                   'pg_conn_id': pg_conn_id,
                   'vertica_conn_id': vertica_conn_id
                   },
        dag=dag
    )

    load_transactions = PythonOperator(
        task_id='load_transactions',
        python_callable=upload_data,
        op_kwargs={'table_name': 'transactions',
                   'dt_column': 'transaction_dt',
                   'pg_conn_id': pg_conn_id,
                   'vertica_conn_id': vertica_conn_id
                   },
        dag=dag
    )

    staging_ddl >> [load_currencies, load_transactions]
