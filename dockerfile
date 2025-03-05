FROM kalilinux/kali-rolling

# Actualizamos el sistema
RUN apt update && apt upgrade -y

# Instalamos herramientas básicas
RUN apt install -y nmap metasploit-framework wordlists net-tools python3-pip git nikto hydra nuclei searchsploit

# Instalamos Spy's Job desde GitHub
RUN git clone https://github.com/XDeadHackerX/The_spy_job.git /opt/Spys-Job

# Copiamos rockyou.txt a una ruta accesible
RUN cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz

# Configuración adicional (puedes añadir herramientas que uses frecuentemente)

# Establecemos la shell por defecto
CMD ["/bin/bash"]
