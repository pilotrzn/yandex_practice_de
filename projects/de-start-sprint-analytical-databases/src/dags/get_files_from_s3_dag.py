from airflow import DAG
import logging
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.decorators import dag
import pendulum
from stg_data_loader import StgLoader
import boto3


vertica_conn = 'vertica_conn'

schema_name = f"{Variable.get('SCHEMA_NAME')}__STAGING"
BUCKET_FILES = ['users.csv', 'groups.csv', 'dialogs.csv']

log = logging.getLogger(__name__)


def load_stg(file_name: str):
    loader = StgLoader(vertica_conn, schema_name, '/data', log)
    loader.load_csv_to_vertica(file_name)


def fetch_s3_file(bucket: str, key: str):
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=Variable.get('ENDPOINT_URL'),
        aws_access_key_id=Variable.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=Variable.get('AWS_SECRET_ACCESS_KEY'),
        )

    s3_client.download_file(
            Bucket=bucket,
            Key=key,
            Filename=f"/data/{key}")


bash_command_tmpl = """
    {% for file in params.files %}
    echo "===== {{ file }} ====="
    cat {{ file }} | head -n 10
    echo ""
    {% endfor %}
"""


@dag(
        schedule_interval=None,
        start_date=pendulum.parse('2022-07-13')
    )
def sprint6_dag_get_data():
    fetch_tasks = []
    load_tasks = []
    for file in BUCKET_FILES:
        task = PythonOperator(
            task_id=f"fetch_{file.replace('.csv', '')}",
            python_callable=fetch_s3_file,
            op_kwargs={
                'bucket': Variable.get('S3_BUCKET'),
                'key': file
            })
        fetch_tasks.append(task)

        load_task = PythonOperator(
            task_id=f"load_{file.replace('.csv', '')}",
            python_callable=load_stg,
            op_kwargs={'file_name': file}
        )
        load_tasks.append(load_task)

    print_10_lines_of_each = BashOperator(
        task_id='print_10_lines_of_each',
        bash_command=bash_command_tmpl,
        params={'files': [f'/data/{f}' for f in BUCKET_FILES]}
    )

    for task in fetch_tasks:
        task >> print_10_lines_of_each

    for task in load_tasks:
        print_10_lines_of_each >> task


_ = sprint6_dag_get_data()
