#!/bin/bash
set -e
cd "$(dirname "$0")/.."
docker compose --profile spark up -d
echo "Lesson 3 infrastructure (spark) started."
