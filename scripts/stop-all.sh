#!/bin/bash
set -e
cd "$(dirname "$0")/.."
docker compose --profile all down
