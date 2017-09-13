from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

from datetime import datetime, timedelta

from job_specific.first.tasks import sqrt_transform
from common_tasks.ml import tpot_regression

default_args = {
    'ownder': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 9, 8),
    'email': ['bradleywgroff@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('first', default_args=default_args, schedule_interval=timedelta(seconds=5))


raw_data_table = 'fakedata'
column = 'y'
tmp_file = '/tmp/rooted'
output_file = '/tmp/tpot.model'

sqrt_task = PythonOperator(
    task_id='sqrt',
    python_callable=sqrt_transform,
    op_kwargs={
        'table': raw_data_table,
        'column': column,
        'tmp_file': tmp_file
    },
    dag=dag)

tpot_task = PythonOperator(
    task_id='tpot',
    python_callable=tpot_regression,
    op_kwargs={
        'data_location': tmp_file,
        'output_location': output_file,
        'target': column + '_root'
    },
    dag=dag)

# email_task = EmailOperator(
#     task_id='sendtobrad',
#     to='bradleywgroff@gmail.com',
#     subject='yodiswrks',
#     html_content='yay!',
#     dag=dag
# )

sqrt_task >> tpot_task
