import datetime as dt
import pandas as pd
import os
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable

from sqlalchemy import create_engine 


POSTGRES_URL = Variable.get('postgres_url')
TLGR_ALERTS = Variable.get('telegram_alerts_chat')

args = {
   'owner': 'airflow',  # Информация о владельце DAG
   'start_date': dt.datetime(2020, 12, 23),  # Время начала выполнения пайплайна
   'retries': 1,  # Количество повторений в случае неудач
   'retry_delay': dt.timedelta(minutes=1),  # Пауза между повторами
}


def get_path(file_name):
   return os.path.join(os.path.expanduser('~'), file_name)


def download_titanic_dataset():
   url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
   df = pd.read_csv(url)
   engine = create_engine(POSTGRES_URL)
   df.to_sql('titanic', engine, index=False, if_exists='replace', schema='datasets')


def pivot_dataset():
   engine = create_engine(POSTGRES_URL)
   titanic_df = pd.read_sql('select * from datasets.titanic', con=engine)
   df = titanic_df.pivot_table(index=['Sex'],
                               columns=['Pclass'],
                               values='Name',
                               aggfunc='count').reset_index()
   
   df.to_sql('titanic_pivot', engine, index=False, if_exists='replace', schema='datasets' )


dag = DAG(dag_id='titanic_pivot_w_alert',  # Имя DAG
    schedule_interval=None,  # Периодичность запуска, например, "00 15 * * *"
    default_args=args,  # Базовые аргументы
)


first_task = BashOperator(
    task_id='first_task',
    bash_command='echo "Here we start! Info: run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag,
)

# делаем группу задач с работой с данными
with TaskGroup(group_id="preprocessing_stage") as preprocessing:
    # Загрузка датасета
    create_titanic_dataset = PythonOperator(
        task_id='download_titanic_dataset',
        python_callable=download_titanic_dataset,
        dag=dag,
    )
    # Чтение, преобразование и запись датасета
    pivot_titanic_dataset = PythonOperator(
        task_id='pivoting_dataset',
        python_callable=pivot_dataset,
        dag=dag,
    )
    create_titanic_dataset >> pivot_titanic_dataset


with TaskGroup(group_id="post_stage") as post_stage:
    send_message_telegram_task = TelegramOperator(
        task_id='send_message_telegram',
        telegram_conn_id='telegram_alerts',
        chat_id=TLGR_ALERTS,
        text="""DAG \`{{ dag_id }}\` with run_id={{ run_id }} is done!""",
        dag=dag)    
    done = DummyOperator(task_id='aggregation_calculated', dag=dag)
    send_message_telegram_task >> done
    
    first_task >> preprocessing >> post_stage