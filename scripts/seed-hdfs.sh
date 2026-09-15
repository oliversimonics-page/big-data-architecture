#!/bin/bash
set -e
cd "$(dirname "$0")/.."
docker compose --profile hdfs up -d namenode datanode1 datanode2
echo "Waiting for HDFS..."
sleep 8
docker compose exec namenode hdfs dfs -mkdir -p /data/raw/sensors /data/reference /data/processed
docker compose exec namenode hdfs dfs -put -f /course-data/historical/sensors.json /data/raw/sensors/sensors.json
docker compose exec namenode hdfs dfs -put -f /course-data/reference/locations.csv /data/reference/locations.csv
echo "Historical data seeded."
