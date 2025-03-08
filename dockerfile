#Cogemos el docker original de kali
FROM kalilinux/kali-rolling

LABEL maintainer="hop_lab"


# Añadimos las herramientas a la maquina (puedes probar a añadir)
RUN apt update && apt upgrade -y && \
    apt install -y exploitdb nmap metasploit-framework wordlists net-tools python3-pip git nikto hydra nuclei dirb nano python3 wfuzz netcat && \
    cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz


# Establecemos la shell por defecto    
CMD ["/bin/bash"]
