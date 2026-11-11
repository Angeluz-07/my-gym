@echo off

:: 1. Si no se pasa ningún argumento, salta directo a la ejecución normal
if "%~1"=="" (
    docker compose --profile web_app_mg up --remove-orphans
) else (
    :: 2. Si se pasa un argumento, incluye el flag --profile
    docker compose --profile %~1 up --remove-orphans
)