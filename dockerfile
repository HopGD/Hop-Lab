FROM kalilinux/kali-rolling

LABEL maintainer="hop-lab"

RUN apt update && apt upgrade -y && \
    apt install -y exploitdb nmap metasploit-framework wordlists net-tools python3-pip git nikto hydra nuclei  dirb nano python3 && \
    cp /usr/share/wordlists/rockyou.txt.gz /root/ && gunzip /root/rockyou.txt.gz

CMD ["/bin/bash"]
