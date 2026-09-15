#!/bin/bash
cd "$(dirname "$0")/.."
docker compose --profile kafka up -d kafka kafka-init spark-master spark-worker1 spark-worker2 spark-kafka-init producer
docker compose exec spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 --jars /opt/spark/packages/spark-sql-kafka-0-10_2.13-4.0.1.jar /opt/spark/jobs/streaming.py
