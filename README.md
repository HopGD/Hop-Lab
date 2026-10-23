# Hop Lab

[🇪🇸 Español](#-español) · [🇬🇧 English](#-english)

---

## 🇪🇸 Español

Kali Linux en Docker, con las herramientas que suelo usar ya instaladas y un menú en Python para no tener que recordar los comandos de Docker. La idea es tener un lab ligero (la imagen pesa mucho menos que una VM) que se levanta, se usa y se apaga con un par de teclas.

### Qué incluye

- **Imagen `hop_lab`** basada en `kalilinux/kali-rolling`, con:

  | Categoría | Herramientas |
  |---|---|
  | Reconocimiento | `nmap`, `arp-scan`, `net-tools` |
  | Explotación | `metasploit-framework`, `sqlmap`, `hydra`, `evil-winrm`, `nikto`, `nuclei` |
  | Web | `dirb`, `dirbuster`, `wfuzz`, `whatweb`, `wpscan`, `gophish` |
  | Post-explotación | `python3-impacket`, `enum4linux` |
  | Forense / estego | `exiftool`, `steghide` |
  | OSINT | `theharvester` |
  | Red anónima | `tor` + `proxychains` (ya configurado con `config/proxychains.conf`) |
  | Utilidades | `git`, `nano`, `python3`, `pip`, `netcat-traditional`, `ftp` |

- Wordlists listas para usar en `/root`: `rockyou.txt` y el directorio de `dirbuster` copiado a `/root/wordlists/`.

- **`Hop_Lab_Manager.py`**: menú interactivo con colores para iniciar, entrar, parar y actualizar el contenedor.

- `config/proxychains.conf`: configuración de proxychains apuntando a Tor.

### Requisitos

- Docker (con el servicio corriendo)
- Python 3
- `colorama` → `pip install colorama`
- En Linux se usa `sudo` para hablar con Docker; en Windows hace falta Docker Desktop arrancado a mano.

### Instalación

```bash
git clone <este-repo>
cd dockerfile

# 1. Construir la imagen (tarda bastante la primera vez)
./constructor.sh          # equivale a: sudo docker build -t hop_lab .

# 2. Dependencia del menú
pip install colorama
```

### Uso

```bash
python3 Hop_Lab_Manager.py
```

| Opción | Acción | Qué hace exactamente |
|---|---|---|
| `1` | Iniciar contenedor | Borra el contenedor `hop_lab` si ya existía y crea uno nuevo con `docker run --network=host --privileged -v $PWD:/home -d hop_lab tail -f /dev/null` |
| `2` | Abrir shell | `docker exec -ti hop_lab /bin/bash` (en Windows lanza `cmd`) |
| `3` | Detener contenedor | `docker stop hop_lab`. El contenedor se conserva |
| `4` | Actualizar + snapshot | `apt update && apt upgrade` dentro del contenedor, guarda el estado con `docker commit`, borra la imagen antigua y deja la nueva como `hop_lab:latest` |
| `5` | Salir | Cierra el menú (no para el contenedor) |

### Cómo funciona el contenedor

- **`--network=host`**: comparte la red del host, así que las herramientas ven tus interfaces y puedes recibir reverse shells sin mapear puertos.
- **`--privileged`**: acceso completo a dispositivos; necesario para cosas como `arp-scan`, capturas o montajes.
- **`-v $PWD:/home`**: el directorio desde el que lanzas el script se monta en `/home` dentro del contenedor. Todo lo que guardes ahí **sí persiste**; lo que escribas fuera de `/home` vive en la capa del contenedor y se pierde al borrarlo.
- El contenedor se queda dormido con `tail -f /dev/null` y tú entras cuando quieras con la opción 2.

### La opción de actualizar (snapshot)

Kali es una distribución *rolling*, así que se desactualiza rápido. La opción `4` hace esto:

1. Arranca el contenedor si no lo está.
2. Ejecuta dentro (como root, sin `sudo`, con `DEBIAN_FRONTEND=noninteractive` para que `dpkg` no se quede esperando preguntas):

   ```bash
   apt-get update && apt-get -y -o Dpkg::Options::=--force-confold upgrade
   ```

3. Congela el contenedor actualizado en una imagen temporal `hop_lab:snapshot-AAAAMMDD-HHMMSS`.
4. Borra el contenedor viejo, mueve el tag `latest` a la imagen nueva y elimina la imagen anterior.
5. Vuelve a levantar el contenedor con la imagen ya actualizada.

Si el `apt` falla, no se toca ninguna imagen: te muestra el error y sigues como estabas.

> ⚠️ Al borrar la imagen anterior **no hay rollback**. Si quieres conservarla, comenta la línea del `docker rmi {vieja_id}` en `actualizar()`.

### Avisos

- Es un entorno `--privileged` con red del host: úsalo en tu máquina de laboratorio, no en producción.
- La imagen borra el estado del contenedor al recrearlo (opción 1) salvo lo que esté en `/home`.
- Usa todo esto solo en sistemas y redes para los que tengas permiso. El resto es ilegal y no es mi problema.

---

## 🇬🇧 English

Kali Linux in Docker, preloaded with the tools I actually use, plus a small Python menu so I don't have to remember Docker commands. The goal is a lightweight lab (the image is far smaller than a VM) you can spin up, use, and shut down in seconds.

### What's inside

- **`hop_lab` image** based on `kalilinux/kali-rolling`, with:

  | Category | Tools |
  |---|---|
  | Recon | `nmap`, `arp-scan`, `net-tools` |
  | Exploitation | `metasploit-framework`, `sqlmap`, `hydra`, `evil-winrm`, `nikto`, `nuclei` |
  | Web | `dirb`, `dirbuster`, `wfuzz`, `whatweb`, `wpscan`, `gophish` |
  | Post-exploitation | `python3-impacket`, `enum4linux` |
  | Forensics / stego | `exiftool`, `steghide` |
  | OSINT | `theharvester` |
  | Anonymity | `tor` + `proxychains` (preconfigured via `config/proxychains.conf`) |
  | Utilities | `git`, `nano`, `python3`, `pip`, `netcat-traditional`, `ftp` |

- Ready-to-use wordlists in `/root`: `rockyou.txt` and the `dirbuster` wordlists copied to `/root/wordlists/`.

- **`Hop_Lab_Manager.py`**: a colored interactive menu to start, enter, stop and update the container.

- `config/proxychains.conf`: proxychains config routing traffic through Tor.

### Requirements

- Docker (daemon running)
- Python 3
- `colorama` → `pip install colorama`
- On Linux the script uses `sudo` for Docker; on Windows you must start Docker Desktop manually.

### Install

```bash
git clone <this-repo>
cd dockerfile

# 1. Build the image (the first build takes a while)
./constructor.sh          # same as: sudo docker build -t hop_lab .

# 2. Menu dependency
pip install colorama
```

### Usage

```bash
python3 Hop_Lab_Manager.py
```

| Option | Action | What it actually does |
|---|---|---|
| `1` | Start container | Removes any existing `hop_lab` container and runs a fresh one with `docker run --network=host --privileged -v $PWD:/home -d hop_lab tail -f /dev/null` |
| `2` | Open shell | `docker exec -ti hop_lab /bin/bash` (falls back to `cmd` on Windows) |
| `3` | Stop container | `docker stop hop_lab`. The container is kept |
| `4` | Update + snapshot | Runs `apt update && apt upgrade` inside the container, commits the state as a new image, deletes the old image and tags the new one as `hop_lab:latest` |
| `5` | Quit | Leaves the menu (it does **not** stop the container) |

### How the container works

- **`--network=host`**: shares the host network, so tools see your interfaces and reverse shells work without port mapping.
- **`--privileged`**: full device access; needed for things like `arp-scan`, packet capture or mounts.
- **`-v $PWD:/home`**: the directory you launch the script from is mounted at `/home` inside the container. Anything there **persists**; anything outside `/home` lives in the container layer and is lost when the container is removed.
- The container idles with `tail -f /dev/null`; you jump in whenever you want with option 2.

### The update option (snapshots)

Kali is a *rolling* distro, so it drifts out of date quickly. Option `4` does this:

1. Starts the container if it isn't running.
2. Runs inside it (as root, no `sudo`, with `DEBIAN_FRONTEND=noninteractive` so `dpkg` never waits for input):

   ```bash
   apt-get update && apt-get -y -o Dpkg::Options::=--force-confold upgrade
   ```

3. Freezes the upgraded container into a temporary image `hop_lab:snapshot-YYYYMMDD-HHMMSS`.
4. Removes the old container, moves the `latest` tag to the new image and deletes the previous image.
5. Restarts the container from the freshly built image.

If `apt` fails, no image is touched: you get the error and everything stays as it was.

> ⚠️ Deleting the old image means **no rollback**. If you want to keep it, comment out the `docker rmi {vieja_id}` line inside `actualizar()`.

### Disclaimer

- This is a `--privileged` container with host networking: run it on your own lab machine, never in production.
- Recreating the container (option 1) wipes its state except whatever lives in `/home`.
- Only use this against systems and networks you are allowed to test. Anything else is illegal, and that's on you.
