from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from data_pipelines.kafka_pull import main
from datetime import datetime
import time

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
    
    task2_1 = PythonOperator(
        task_id="backblaze-smart-kafka-pull",
        python_callable = main,
        op_kwargs={
            "topic": "backblaze_smart",
            "group_id": "backblaze-smart-consumer",
            "max_duration": 60,
            "bucket": "kafka-lenses-raw",
            "prefix": "backblaze_smart",
            "file_name_prefix": "backblaze_smart",
            "format": "json"
        }
    )
    
    task2_2 = PythonOperator(
        task_id="telecom-italia-data-kafka-pull",
        python_callable = main,
        op_kwargs={
            "topic": "telecom_italia_data",
            "group_id": "telecom-italia-data-consumer-group",
            "max_duration": 60,
            "auto_offset_reset": "earliest",
            "bucket": "kafka-lenses-raw",
            "prefix": "telecom_italia_data",
            "file_name_prefix": "telecom_italia_data",
            "format": "avro",
            "schema_file": "http://demo-kafka:8081"
        }
    )
    
    task2_3 = PythonOperator(
        task_id="nyc-yellow-taxi-trip-data-kafka-pull",
        python_callable = main,
        op_kwargs={
            "topic": "nyc_yellow_taxi_trip_data",
            "group_id": "nyc-yellow-taxi-trip-data-consumer",
            "max_duration": 60,
            "bucket": "kafka-lenses-raw",
            "prefix": "nyc_yellow_taxi_trip_data",
            "file_name_prefix": "nyc_yellow_taxi_trip_data",
            "format": "avro",
            "schema_file": "http://demo-kafka:8081"
        }
    )
    
    task2_4 = PythonOperator(
        task_id="sea-vessel-position-reports-kafka-pull",
        python_callable = main,
        op_kwargs={
            "topic": "sea_vessel_position_reports",
            "group_id": "sea-vessel-position-reports-consumer",
            "max_duration": 60,
            "bucket": "kafka-lenses-raw",
            "prefix": "sea_vessel_position_reports",
            "file_name_prefix": "sea_vessel_position_reports",
            "format": "avro",
            "schema_file": "http://demo-kafka:8081"
        }
    )
    
    task2_5 = PythonOperator(
        task_id="telecom-italia-grid-kafka-pull",
        python_callable = main,
        op_kwargs={
            "topic": "telecom_italia_grid",
            "group_id": "telecom-italia-grid-consumer",
            "max_duration": 60,
            "bucket": "kafka-lenses-raw",
            "prefix": "telecom_italia_grid",
            "file_name_prefix": "telecom_italia_grid",
            "format": "avro",
            "schema_file": "http://demo-kafka:8081"
        }
    )
    
    task2_6 = PythonOperator(
        task_id="logs-broker-kafka-pull",
        python_callable = main,
        op_kwargs={
            "topic": "logs_broker",
            "group_id": "logs-broker-consumer",
            "max_duration": 60,
            "bucket": "kafka-lenses-raw",
            "prefix": "logs_broker",
            "file_name_prefix": "logs_broker",
            "format": "avro",
            "schema_file": "http://demo-kafka:8081"
        }
    )

    task3 = BashOperator(
        task_id="kafka-turn-off-lenses",
        bash_command="docker compose -f /opt/airflow/data-pipelines/docker-compose.yml down"
    )


task1 >> (task2_1, task2_2, task2_3, task2_4, task2_5, task2_6) >> task3