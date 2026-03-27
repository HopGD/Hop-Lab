#!/bin/bash

# Script constructor para Hop-Lab con Docker Compose

set -e

echo "=========================================="
echo "  Hop-Lab Constructor"
echo "=========================================="
echo ""

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "[+] Creando .env desde .env.example..."
    cp .env.example .env
    echo "[!] Por favor, revisa el archivo .env y personaliza las credenciales"
fi

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "[X] Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "[X] Docker Compose no está instalado"
    exit 1
fi

echo "[+] Construyendo imagen..."
docker-compose build

echo ""
echo "[+] Imagen construida correctamente!"
echo ""
echo "Para iniciar el lab:"
echo "  docker-compose up -d"
echo ""
echo "Para ver logs:"
echo "  docker-compose logs -f"
echo ""
echo "Para detener:"
echo "  docker-compose down"
echo ""
echo "Para abrir un terminal:"
echo "  docker exec -it hop_lab /bin/zsh"
echo ""
