from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
# from data_pipelines.etl_ingestion import main
from datetime import datetime

with DAG(
    dag_id="kafka-lenses-ingestion",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    task1 = SparkSubmitOperator(
        task_id="kafka-backblaze_smart-etl-ingestion",
        application = "/opt/airflow/data-pipelines/data_pipelines/etl_ingestion.py",
        conn_id="spark_default", 
        name="kafka_backblaze_smart_job",
        verbose=True
    )