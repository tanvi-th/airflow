import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from data_pipelines.kafka_pull import main
from datetime import datetime

with DAG(
    dag_id="kafka-lenses-data-pull",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
) as dag:
    task1 = BashOperator(
        task_id="kafka-spin-up-lenses",
        bash_command="""
            export ACCEPT_EULA=true
            docker compose -f /opt/airflow/data-pipelines/docker-compose.yml up -d --wait
        """
)
    
    task2 = PythonOperator(
        task_id="kafka-pull",
        python_callable = main
    )
    
    task3 = BashOperator(
        task_id="kafka-turn-off-lenses",
        bash_command="docker compose -f /opt/airflow/data-pipelines/docker-compose.yml down"
    )


task1 >> task2 >> task3