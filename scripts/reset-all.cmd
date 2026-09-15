@echo off
cd /d "%~dp0.."
docker compose --profile all down -v
