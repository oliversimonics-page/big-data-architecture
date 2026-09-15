@echo off
cd /d "%~dp0.."
docker compose --profile spark up -d
