# Usamos Alpine para evitar los errores de repositorios de Debian antiguo
FROM python:3.8-alpine

# Instalamos las herramientas de compilación necesarias en Alpine
RUN apk add --no-cache \
    binutils \
    build-base \
    tk-dev \
    tcl-dev \
    zlib-dev \
    jpeg-dev

# Instalamos las librerías de Python
RUN pip install --no-cache-dir customtkinter Pillow pyinstaller

WORKDIR /app
COPY . .

# Generamos el ejecutable en modo carpeta (Onedir)
CMD pyinstaller --noconsole --clean --name "TPV_Bar" \
    --add-data "menu.json:." \
    --add-data "Images:Images" \
    main.py