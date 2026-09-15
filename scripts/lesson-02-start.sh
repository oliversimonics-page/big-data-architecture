#!/bin/bash
set -e
cd "$(dirname "$0")/.."
docker compose --profile spark up -d
echo "Lesson 2 infrastructure (spark) started."
