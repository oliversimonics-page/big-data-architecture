@echo off
cd /d "%~dp0.."
docker compose --profile all up -d
