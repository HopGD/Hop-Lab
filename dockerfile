#Cogemos el docker original de kali
FROM kalilinux/kali-rolling

LABEL maintainer="Hop"

# Añadimos las herramientas a la máquina
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nmap metasploit-framework exploitdb wordlists net-tools python3 python3-pip python3-setuptools git nikto hydra nuclei dirb wfuzz netcat-traditional dirbuster sqlmap theharvester gophish enum4linux ftp exiftool steghide whatweb arp-scan evil-winrm wpscan python3-impacket gobuster ffuf amass subfinder crackmapexec bloodhound python3-ldapdomaindump certipy-ad john hashcat socat seclists tmux zsh figlet lolcat && \
    cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz && \
    cp -r /usr/share/dirbuster/ /root/wordlists/

# Instalamos pspy (no esta en repos de Kali, descargamos binario)
RUN curl -L https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64 -o /usr/local/bin/pspy && \
    chmod +x /usr/local/bin/pspy

# Instalamos tambien tor y proxychains
RUN apt -y install tor proxychains
COPY config/proxychains.conf /etc/proxychains.conf

# Instalamos micro (editor moderno)
RUN curl https://getmic.ro | bash && mv micro /usr/local/bin/

# === XFCE + VNC + noVNC ===
# Entorno de escritorio XFCE
RUN apt-get install -y \
    xfce4 xfce4-goodies \
    tigervnc-standalone-server tigervnc-viewer tigervnc-tools \
    novnc websockify \
    dbus-x11 \
    fonts-noto \
    --no-install-recommends

# Herramientas graficas adicionales
RUN apt-get install -y firefox-esr burpsuite

# Configuracion de zsh para root
COPY config/.zshrc /root/.zshrc

# Configuracion de zsh para usuarios (se copiara al crear usuario)
RUN mkdir -p /etc/skel
COPY config/.zshrc /etc/skel/.zshrc

# Script de inicio
COPY config/start-services.sh /opt/start-services.sh
RUN chmod +x /opt/start-services.sh

# Puerto para noVNC (nota: con network_mode: host no se usa EXPOSE realmente)
EXPOSE 6080 5901

CMD ["/bin/zsh"]
