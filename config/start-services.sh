#!/bin/bash

# Script de inicio para Hop-Lab

# Variables con valores por defecto
USER=${USER:-hoplab}
PASS=${PASS:-hoplab123}
VNC_PASS=${VNC_PASS:-kalilab}

# Iniciar dbus (necesario para XFCE)
/etc/init.d/dbus start 2>/dev/null || service dbus start 2>/dev/null

# Crear usuario si no existe
if ! id "$USER" &>/dev/null; then
    echo "[+] Creando usuario: $USER"
    useradd -m -s /bin/zsh -G sudo $USER
    echo "$USER:$PASS" | chpasswd
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
fi

# Configurar VNC para el usuario
USER_HOME="/home/$USER"
mkdir -p $USER_HOME/.vnc

# Crear archivo xstartup para XFCE
cat > $USER_HOME/.vnc/xstartup << 'EOF'
#!/bin/bash
xrdb $HOME/.Xresources 2>/dev/null
startxfce4 &
EOF
chmod +x $USER_HOME/.vnc/xstartup

# Establecer password VNC (maximo 8 caracteres para TigerVNC)
echo "$VNC_PASS" | vncpasswd -f > $USER_HOME/.vnc/passwd
chmod 600 $USER_HOME/.vnc/passwd
chown -R $USER:$USER $USER_HOME

# Limpiar sesiones VNC previas (por si el contenedor se reinicia)
su - $USER -c "vncserver -kill :1 2>/dev/null || true"
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1 2>/dev/null

# Iniciar VNC como el usuario (solo localhost)
su - $USER -c "vncserver :1 -geometry 1920x1080 -depth 24 -localhost yes -passwd $USER_HOME/.vnc/passwd"

# Esperar a que VNC esté listo
sleep 3

# Iniciar noVNC (escucha en 127.0.0.1:6080)
/usr/share/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080 &

echo ""
echo "=========================================="
echo "  Hop-Lab iniciado correctamente!"
echo "=========================================="
echo ""
echo "  Usuario: $USER"
echo "  Password: $PASS"
echo "  VNC Pass: $VNC_PASS"
echo ""
echo "  Acceso Web: http://127.0.0.1:6080/vnc.html"
echo "  VNC Directo: localhost:5901"
echo ""
echo "=========================================="
echo ""

# Mantener el contenedor corriendo
tail -f /dev/null
