#Cogemos el docker original de kali
FROM kalilinux/kali-rolling

LABEL maintainer="Hop"

# Añadimos las herramientas a la máquina (puedes probar a añadir)
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nmap metasploit-framework exploitdb wordlists net-tools python3 python3-pip python3-setuptools git nikto hydra nuclei dirb nano wfuzz netcat-traditional dirbuster sqlmap theharvester gophish enum4linux ftp exiftool steghide whatweb arp-scan evil-winrm wpscan python3-impacket && \
    cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz && \
    cp -r /usr/share/dirbuster/ /root/wordlists/

# Instalamos tambien tor y proxychains y configuramos proxychains con tor
RUN apt -y install tor proxychains
COPY config/proxychains.conf /etc/proxychains.conf


# Establecemos la shell por defecto    
CMD ["/bin/bash"]
