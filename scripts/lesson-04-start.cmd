@echo off
cd /d "%~dp0.."
docker compose --profile streaming up -d
