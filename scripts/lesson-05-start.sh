#!/bin/bash
set -e
cd "$(dirname "$0")/.."
docker compose --profile kafka up -d
echo "Lesson 5 infrastructure (kafka) started."
