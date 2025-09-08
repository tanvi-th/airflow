from apache/airflow:2.9.3

USER root
COPY data-pipelines /opt/data-pipelines
RUN chown -R airflow: /opt/data-pipelines /opt



RUN apt-get update && \
    apt-get install -y \
        docker.io \
        docker-compose-plugin \
        curl && \
    rm -rf /var/lib/apt/lists/*


RUN usermod -aG docker airflow

USER airflow

WORKDIR /opt/data-pipelines
RUN pip install --no-cache-dir build && python -m build --wheel -o /opt/dist
WORKDIR /opt/airflow
RUN pip install --no-cache-dir  /opt/dist/*.whl

