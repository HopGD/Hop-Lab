#Cogemos el docker original de kali
FROM kalilinux/kali-rolling

LABEL maintainer="Hop"

# Añadimos las herramientas a la máquina (puedes probar a añadir)
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nmap metasploit-framework exploitdb wordlists net-tools python3 python3-pip python3-setuptools git nikto hydra nuclei dirb nano wfuzz netcat-traditional dirbuster sqlmap theharvester gophish enum4linux ftp exiftool steghide && \
    cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz && \
    cp -r /usr/share/dirbuster/ /root/wordlists/ && \
    useradd -m kaliuser && echo "kaliuser:kali" | chpasswd && \
    echo 'startxfce4' > /home/kaliuser/.xsession && chown kaliuser:kaliuser /home/kaliuser/.xsession

# Instalamos tambien tor y proxychains y configuramos proxychains con tor
RUN apt -y install tor proxychains
COPY config/proxychains.conf /etc/proxychains.conf


# Establecemos la shell por defecto    
CMD service ssh start && /bin/bash
