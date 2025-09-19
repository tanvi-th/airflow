from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
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
        conf={
                "spark.driver.extraJavaOptions": "-Dlog4j.rootCategory=INFO,console",
                "spark.executor.extraJavaOptions": "-Dlog4j.rootCategory=INFO,console",
                "spark.submit.verbose": "true",
                "spark.eventLog.enabled": "true",
                "spark.eventLog.dir": "file:/opt/spark/logs",
                "spark.ui.enabled": "true",
                "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
                "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
            },
        verbose=True,
        env_vars={
        "SPARK_PRINT_LAUNCH_COMMAND": "1"
        },
        jars="/opt/spark/jars/hadoop-aws-3.3.4.jar,/opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar,/opt/spark/jars/delta-spark_2.12-3.2.0.jar,/opt/spark/jars/delta-storage-3.2.0.jar"
)