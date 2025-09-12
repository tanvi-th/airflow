FROM apache/airflow:2.10.2-python3.9

ARG AIRFLOW_VERSION=2.10.2
ARG PYTHON_VERSION=3.9
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

USER root
COPY data-pipelines /opt/data-pipelines
COPY airflow/spark-3.5.6-bin-hadoop3.tgz /tmp/

# install system deps
RUN mkdir -p /opt/airflow /opt/airflow/logs /opt/airflow/dags /opt/airflow/plugins && \
    chown -R airflow:0 /opt/airflow
RUN set -eux && \
    chown -R airflow: /opt/data-pipelines /opt && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jdk \
        docker.io \
        docker-compose-plugin \
        curl && \
    rm -rf /var/lib/apt/lists/* && \
    # Add airflow user to docker group
    usermod -aG docker airflow && \
    # Install Spark
    tar -xzf /tmp/spark-3.5.6-bin-hadoop3.tgz -C /opt && \
    ln -sf /opt/spark-3.5.6-bin-hadoop3 /opt/spark && \
    rm /tmp/spark-3.5.6-bin-hadoop3.tgz

USER airflow

# Environment variables
ENV SPARK_HOME=/opt/spark \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    PATH="/usr/lib/jvm/java-17-openjdk-arm64/bin:/home/airflow/.local/bin:/opt/airflow/venv/bin:/opt/spark/bin:$PATH" \
    AIRFLOW_HOME=/opt/airflow

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --constraint "${CONSTRAINT_URL}" apache-airflow-providers-apache-spark

WORKDIR /opt/data-pipelines
RUN pip install --no-cache-dir build && python -m build --wheel -o /opt/dist

WORKDIR /opt/airflow
RUN pip install --no-cache-dir  /opt/dist/*.whl