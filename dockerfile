#Cogemos el docker original de kali
FROM kalilinux/kali-rolling

LABEL maintainer="Hop"

# Añadimos las herramientas a la maquina (puedes probar a añadir)
RUN apt update && apt upgrade -y && \
    apt install -y nmap metasploit-framework exploitdb wordlists net-tools python3 python3-pip python3-setuptools git nikto hydra nuclei dirb nano wfuzz netcat-traditional dirbuster sqlmap theharvester && \
    cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz && \
    cp -r /usr/share/dirbuster/ /root/wordlists/


# Instalamos tambien tor y proxychains y configuramos proxychains con tor
RUN apt -y install tor proxychains
COPY config/proxychains.conf /etc/proxychains.conf


# Establecemos la shell por defecto    
CMD ["/bin/bash"]
