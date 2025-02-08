import datetime as dt
import os
import sys
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from modules.pipeline import pipeline
from modules.predict import predict
path = os.path.expanduser('~/airflow_hw')
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)

args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
        dag_id='car_price_prediction',
        schedule_interval=None,
        default_args=args,
        catchup=False,
) as dag:
    pipeline_task = PythonOperator(
        task_id='pipeline',
        python_callable=pipeline,
        dag=dag
    )
    predict_task = PythonOperator(
        task_id='run_predictions',
        python_callable=predict,
        dag=dag
    )

    pipeline_task >> predict_task
