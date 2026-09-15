@echo off
cd /d "%~dp0.."
docker compose --profile hdfs up -d
