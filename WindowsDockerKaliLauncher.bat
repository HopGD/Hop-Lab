@echo off
:: Nombre del contenedor
set CONTAINER_NAME=hop_lab

:: Verifica si el contenedor existe
docker ps -a --format "{{.Names}}" | findstr /I "%CONTAINER_NAME%" > nul
if %errorlevel% neq 0 (
    echo No se encontró el contenedor. Creándolo...
    docker run -dit --name %CONTAINER_NAME% --network host hop_lab
) else (
    echo Contenedor encontrado. Iniciándolo...
    docker start %CONTAINER_NAME% > nul
)

:: Abre una nueva sesión en el contenedor
docker exec -it %CONTAINER_NAME% cmd