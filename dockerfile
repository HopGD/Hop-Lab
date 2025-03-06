FROM kalilinux/kali-rolling

# Actualizamos el sistema
RUN apt update && apt upgrade -y  && \
    apt install -y nmap metasploit-framework wordlists net-tools python3-pip git nikto hydra nuclei exploitdb && \
    cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz

# Establecemos la shell por defecto
CMD ["/bin/bash"]
