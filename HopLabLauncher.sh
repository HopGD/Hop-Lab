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

# Comprueba si ya hay sesiones abiertas
if docker exec $CONTAINER_NAME ps aux | grep -q "[b]ash"; then
    echo "Ya hay una sesión abierta, conectando a la existente..."
else
    echo "No hay sesiones abiertas, abriendo una nueva..."
fi

# Abre la sesión
docker exec -ti $CONTAINER_NAME /bin/bash

# Si la sesión termina, revisa si hay más sesiones activas
if ! docker exec $CONTAINER_NAME ps aux | grep -q "[b]ash"; then
    echo "No quedan sesiones activas, apagando el contenedor..."
    docker stop $CONTAINER_NAME
fi
