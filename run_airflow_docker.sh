#!/bin/bash
set -x  

docker compose down -v --remove-orphans
docker compose build --no-cache
docker compose up airflow-init
docker compose up -d