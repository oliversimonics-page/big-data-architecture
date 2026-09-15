#!/bin/bash
set -e
cd "$(dirname "$0")/.."
docker compose --profile streaming up -d
echo "Lesson 4 infrastructure (streaming) started."
