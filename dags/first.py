from airflow import DAG
from airflow.operators.python_operator import PythonOperator
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


raw_data = 0
column = 0
data_location = 0
output_location = 0

sqrt_task = PythonOperator(
    task_id='sqrt',
    python_callable=sqrt_transform,
    op_kwargs={
        'data_location': raw_data,
        'column': column
    },
    dag=dag)

tpot_task = PythonOperator(
    task_id='tpot',
    python_callable=tpot_regression,
    op_kwargs={
        'data_location': data_location,
        'output_location': output_location
    },
    dag=dag)

sqrt_task >> tpot_task
