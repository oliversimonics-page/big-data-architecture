@echo off
cd /d "%~dp0.."
docker compose --profile kafka up -d
