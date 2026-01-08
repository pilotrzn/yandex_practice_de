from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
import pendulum
import logging


log = logging.getLogger(__name__)

vertica_conn_id = 'vertica_conn'
business_dt = '{{ ds }}'
args = {
    "owner": "grant5518",
    'retries': 3
}

with DAG(
    dag_id='update_datamart',
    default_args=args,
    schedule_interval='@daily',
    start_date=pendulum.parse('2022-10-01'),
    end_date=pendulum.parse('2022-11-02'),
    catchup=True,
    tags=['final_project', 'update_mart', 'stg_to_dwh', 'vertica']
) as dag:

    external_task_sensor = ExternalTaskSensor(
        task_id='external_task_sensor',
        timeout=30,
        retries=2,
        external_dag_id='upload_data',
        dag=dag
        )

    dwh_ddl = SQLExecuteQueryOperator(
        task_id='dwh_ddl',
        conn_id=vertica_conn_id,
        database='Vertica',
        sql='sql/ddl_vertica_dwh.sql'
    )

    mart_update = SQLExecuteQueryOperator(
        task_id='mart_update',
        conn_id=vertica_conn_id,
        database='Vertica',
        sql='sql/update_metrica.sql'
    )

    external_task_sensor >> dwh_ddl >> mart_update
