#!/bin/bash
set -e
cd "$(dirname "$0")/.."
docker compose --profile hdfs up -d
echo "Lesson 1 infrastructure (hdfs) started."
