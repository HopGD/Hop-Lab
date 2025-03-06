#!/bin/bash

CONTAINER_NAME="hop_lab"

# Comprueba si el contenedor está corriendo
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "El contenedor no está en ejecución. Iniciando..."
    docker start $CONTAINER_NAME 2>/dev/null || {
        echo "El contenedor no existe, creando e iniciando..."
        docker run -ti --name $CONTAINER_NAME $CONTAINER_NAME
        exit 0
    }
    sleep 2
fi

# Abre una nueva sesión en el contenedor
echo "Abriendo nueva sesión en $CONTAINER_NAME..."
docker exec -ti $CONTAINER_NAME /bin/bash
