import airflow
import os
from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


SPARK_CONF = {
    'spark.executor.memory': '4G',
    'spark.executor.cores': '2',
    'spark.executor.instances': '5',
    'spark.driver.memory': '3G',
    'spark.driver.maxResultSize': '20G',
    'spark.yarn.queue': 'default',
    'spark.submit.deployMode': 'cluster'
}

# Настройка окружения
os.environ['HADOOP_CONF_DIR'] = '/etc/hadoop/conf'
os.environ['YARN_CONF_DIR'] = '/etc/hadoop/conf'
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
os.environ['SPARK_HOME'] = '/usr/lib/spark'
os.environ['PYTHONPATH'] = '/usr/bin/python3'

default_args = {
    'start_date': datetime(2025, 5, 20),
    'owner': 'airflow'
}

dag = DAG(
    "events_mart_dag",
    default_args=default_args,
    description='Ежедневная обработка данных с откатом на 3 года',
    schedule_interval='0 0 * * *',
    max_active_runs=1
)


user_geo = SparkSubmitOperator(
    task_id='users_geo_mart_job',
    name='users_geo_mart_processing_{{ ds }}',
    conn_id='yarn_spark',
    verbose=False,
    conf=SPARK_CONF,
    application='scripts/1_task_user_geo.py',
    application_args=[
       "{{ execution_date.replace(year=execution_date.year - 3).strftime('%Y-%m-%d') }}",
       '/user/master/data/geo',
       '/user/pilotryaza/data/geo_tz.csv',
       '/user/pilotryaza/analytics/users_geo_mart'
    ],
    dag=dag,
)

zones_types = SparkSubmitOperator(
    task_id='zones_types_mart_job',
    name='zones_types_mart_processing_{{ ds }}',
    conn_id='yarn_spark',
    verbose=False,
    conf=SPARK_CONF,
    application='scripts/2_task_zones.py',
    application_args=[
       "{{ execution_date.replace(year=execution_date.year - 3).strftime('%Y-%m-%d') }}",
       '/user/master/data/geo',
       '/user/pilotryaza/data/geo_tz.csv',
       '/user/pilotryaza/analytics/users_geo_mart',
       '/user/pilotryaza/analytics/zones_mart'
    ],
    dag=dag,
)

recomendations = SparkSubmitOperator(
    task_id='recomendations_mart_job',
    name='recomendations_mart_processing_{{ ds }}',
    conn_id='yarn_spark',
    verbose=False,
    conf=SPARK_CONF,
    application='scripts/3_task_recommended.py',
    application_args=[
       "{{ execution_date.replace(year=execution_date.year - 3).strftime('%Y-%m-%d') }}",
       '/user/master/data/geo',
       '/user/pilotryaza/data/geo_tz.csv',
       '/user/pilotryaza/analytics/users_geo_mart',
       '/user/pilotryaza/analytics/recommendation_mart'
    ],
    dag=dag,
)


user_geo >> zones_types >> recomendations
