$ErrorActionPreference="Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
docker compose exec spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/jobs/batch.py
