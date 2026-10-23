import subprocess
import sys
import threading
import time
from colorama import init, Fore, Style

init(autoreset=True)

#   Variables:

CONTAINER_NAME = "hop_lab"
IMAGE_NAME = "hop_lab"  # Cambia si tu imagen tiene otro nombre
sudo_prefix = "sudo " if not sys.platform.startswith("win") else "" # Necesario para la compatibilidad linux

# Funciones: 

# Spinner simple
def spinner(proc):
    spin_chars = ['▓', '▒', '░', '▒']
    i = 0
    while proc.poll() is None:
        sys.stdout.write(f"\r{Fore.CYAN}▸{Style.RESET_ALL} Procesando... {Fore.CYAN}{spin_chars[i % 4]}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print(f"\r{Fore.GREEN}✓{Style.RESET_ALL} Operación completada{Style.RESET_ALL}          ")

# Ejecutar comando con spinner y devolver tambien el código de salida
def run_cmd_full(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    spin_thread = threading.Thread(target=spinner, args=(proc,))
    spin_thread.start()
    stdout, stderr = proc.communicate()
    spin_thread.join()
    return stdout.decode().strip(), stderr.decode().strip(), proc.returncode

# Ejecutar comando con spinner
def run_cmd(cmd):
    stdout, stderr, _ = run_cmd_full(cmd)
    return stdout, stderr

# Función para verificar si Docker está corriendo y levantarlo si es necesario
def verificar_docker():
    print(f"{Fore.CYAN}> Verificando servicios del sistema...{Style.RESET_ALL}")
    try:
        subprocess.check_call(f"{sudo_prefix}docker info", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}✓ Docker: ONLINE{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        print(f"{Fore.YELLOW}⚠ Docker: OFFLINE{Style.RESET_ALL}")
        if not sys.platform.startswith("win"):
            print(f"{Fore.CYAN}> Intentando levantar servicios...{Style.RESET_ALL}")
            out, err = run_cmd(f"{sudo_prefix}systemctl start docker")
            try:
                subprocess.check_call(f"{sudo_prefix}docker info", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{Fore.GREEN}✓ Servicios iniciados correctamente{Style.RESET_ALL}")
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}✖ ERROR: No se pudo iniciar Docker{Style.RESET_ALL}")
                if err: print(f"{Fore.RED}✖ Error: {err}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✖ En Windows, inicia Docker Desktop manualmente{Style.RESET_ALL}")

# Función para iniciar el contenedor
def iniciar():
    out, _ = run_cmd(f'{sudo_prefix}docker ps -a -q -f "name=^{CONTAINER_NAME}$"')
    if out:
        print(f"{Fore.YELLOW}⚠ Contenedor existente detectado, purging...{Style.RESET_ALL}")
        run_cmd(f"{sudo_prefix}docker rm -f {CONTAINER_NAME}")
        time.sleep(0.3)

    print(f"{Fore.GREEN}> Ejecutando protocolo de inicio...{Style.RESET_ALL}")
    current_dir = subprocess.getoutput("pwd") if not sys.platform.startswith("win") else subprocess.getoutput("cd")
    run_cmd([
        f"{sudo_prefix}docker run --network=host --privileged --name {CONTAINER_NAME} "
        f"-v {current_dir}:/home -d {IMAGE_NAME} tail -f /dev/null"
    ])
    print(f"{Fore.GREEN}✓ Contenedor [{Fore.CYAN}{CONTAINER_NAME}{Fore.GREEN}] iniciado exitosamente{Style.RESET_ALL}")

# Abrir shell interactivo en contenedor
def abrir_shell():
    out, _ = run_cmd(f'{sudo_prefix}docker ps -q -f "name=^{CONTAINER_NAME}$"')
    if not out:
        print(f"{Fore.RED}✖ ERROR: Contenedor no está en ejecución{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ℹ Ejecuta la opción 1 primero{Style.RESET_ALL}")
        return
    print(f"{Fore.CYAN}> Estableciendo conexión segura...{Style.RESET_ALL}")
    shell_cmd = f"{sudo_prefix}docker exec -ti {CONTAINER_NAME} cmd" if sys.platform.startswith("win") else f"{sudo_prefix}docker exec -ti {CONTAINER_NAME} /bin/bash"
    subprocess.run(shell_cmd, shell=True)

# Detener contenedor
def detener():
    out, _ = run_cmd(f'{sudo_prefix}docker ps -q -f "name=^{CONTAINER_NAME}$"')
    if not out:
        print(f"{Fore.YELLOW}⚠ Contenedor ya se encuentra inactivo{Style.RESET_ALL}")
        return
    print(f"{Fore.MAGENTA}> Deteniendo servicios y cerrando contenedor...{Style.RESET_ALL}")
    run_cmd(f"{sudo_prefix}docker stop {CONTAINER_NAME}")
    print(f"{Fore.MAGENTA}✓ Contenedor detenido y recursos liberados{Style.RESET_ALL}")

# Actualizar paquetes del contenedor, guardar snapshot y reemplazar la imagen antigua
def actualizar():
    print(f"{Fore.YELLOW}> Comprobando estado del contenedor...{Style.RESET_ALL}")

    existe, _ = run_cmd(f'{sudo_prefix}docker ps -a -q -f "name=^{CONTAINER_NAME}$"')
    if not existe:
        print(f"{Fore.YELLOW}⚠ No existe el contenedor, creándolo antes de actualizar...{Style.RESET_ALL}")
        iniciar()
    else:
        en_marcha, _ = run_cmd(f'{sudo_prefix}docker ps -q -f "name=^{CONTAINER_NAME}$"')
        if not en_marcha:
            print(f"{Fore.CYAN}> Contenedor inactivo, arrancándolo para actualizar...{Style.RESET_ALL}")
            run_cmd(f"{sudo_prefix}docker start {CONTAINER_NAME}")
            time.sleep(0.5)

    # Guardamos la referencia de la imagen actual antes de tocarla (para poder borrarla luego)
    vieja_id, _, _ = run_cmd_full(f"{sudo_prefix}docker images -q {IMAGE_NAME}:latest")
    snapshot = f"{IMAGE_NAME}:snapshot-{time.strftime('%Y%m%d-%H%M%S')}"

    # Dentro del contenedor somos root, así que no hace falta sudo.
    # DEBIAN_FRONTEND + force-confold evitan que dpkg se quede esperando respuestas.
    comando_apt = (
        "export DEBIAN_FRONTEND=noninteractive; "
        "apt-get update && "
        "apt-get -y -o Dpkg::Options::=--force-confold upgrade"
    )
    print(f"{Fore.CYAN}> Actualizando paquetes dentro del contenedor (puede tardar, no interrumpas)...{Style.RESET_ALL}")
    _, err, rc = run_cmd_full(f'{sudo_prefix}docker exec {CONTAINER_NAME} bash -lc "{comando_apt}"')
    if rc != 0:
        print(f"{Fore.RED}✖ ERROR: falló la actualización dentro del contenedor{Style.RESET_ALL}")
        if err:
            print(f"{Fore.RED}{err[-800:]}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ℹ No se ha modificado ninguna imagen{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}> Guardando snapshot del contenedor actualizado...{Style.RESET_ALL}")
    _, err, rc = run_cmd_full(f"{sudo_prefix}docker commit {CONTAINER_NAME} {snapshot}")
    if rc != 0:
        print(f"{Fore.RED}✖ ERROR: no se pudo crear el snapshot{Style.RESET_ALL}")
        if err:
            print(f"{Fore.RED}{err[-800:]}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ℹ La imagen antigua sigue intacta{Style.RESET_ALL}")
        return

    print(f"{Fore.MAGENTA}> Reemplazando imagen antigua por la actualizada...{Style.RESET_ALL}")
    run_cmd(f"{sudo_prefix}docker stop {CONTAINER_NAME}")
    run_cmd(f"{sudo_prefix}docker rm {CONTAINER_NAME}")

    # El snapshot pasa a ser la imagen oficial (latest) y luego se borra la antigua
    _, err, rc = run_cmd_full(f"{sudo_prefix}docker tag {snapshot} {IMAGE_NAME}:latest")
    if rc != 0:
        print(f"{Fore.RED}✖ ERROR: no se pudo etiquetar la imagen nueva como {IMAGE_NAME}:latest{Style.RESET_ALL}")
        if err:
            print(f"{Fore.RED}{err[-800:]}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ℹ El snapshot se conserva como {snapshot}{Style.RESET_ALL}")
        return

    run_cmd(f"{sudo_prefix}docker rmi {snapshot}")  # quita el tag temporal, la imagen queda como latest

    nueva_id, _, _ = run_cmd_full(f"{sudo_prefix}docker images -q {IMAGE_NAME}:latest")
    if vieja_id and vieja_id != nueva_id:
        _, err, rc = run_cmd_full(f"{sudo_prefix}docker rmi {vieja_id}")
        if rc != 0:
            print(f"{Fore.YELLOW}⚠ No se pudo borrar la imagen antigua (puede estar en uso){Style.RESET_ALL}")
            if err:
                print(f"{Fore.YELLOW}{err[-400:]}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✓ Imagen antigua eliminada ({vieja_id[:12]}){Style.RESET_ALL}")

    print(f"{Fore.GREEN}✓ Snapshot guardado como {Fore.CYAN}{IMAGE_NAME}:latest{Style.RESET_ALL}")
    print(f"{Fore.CYAN}> Levantando contenedor con la imagen actualizada...{Style.RESET_ALL}")
    iniciar()

def banner():
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║ m    m  mmmm  mmmmm  m        mm   mmmmm                 ║
║ #    # m"  "m #   "# #        ##   #    #                ║
║ #mmmm# #    # #mmm#" #       #  #  #mmmm"                ║
║ #    # #    # #      #       #mm#  #    #                ║
║ #    #  #mm#  #      #mmmmm #    # #mmmm"                ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  > SISTEMA DE GESTIÓN DE CONTENEDORES v2.0.77            ║
║  > MODO: {Fore.GREEN}HACKER{Style.RESET_ALL}{Fore.CYAN} | CONEXIÓN: {Fore.GREEN}SEGURA{Style.RESET_ALL}{Fore.CYAN}                       ║
╚══════════════════════════════════════════════════════════╝
""")

def menu():
    verificar_docker()
    banner()
    time.sleep(0.5)
    while True:
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║  {Fore.MAGENTA}▓▓▓▓▓ MENÚ PRINCIPAL ▓▓▓▓▓{Fore.CYAN}                              ║
╠══════════════════════════════════════════════════════════╣
║  {Fore.GREEN}[1]{Style.RESET_ALL} ▸ INICIAR CONTENEDOR     [{Fore.GREEN}▲{Style.RESET_ALL}]                        ║
║  {Fore.CYAN}[2]{Style.RESET_ALL} ▸ ABRIR SHELL INTERACTIVO [{Fore.CYAN}◈{Style.RESET_ALL}]                       ║
║  {Fore.MAGENTA}[3]{Style.RESET_ALL} ▸ DETENER CONTENEDOR    [{Fore.MAGENTA}▼{Style.RESET_ALL}]                         ║
║  {Fore.YELLOW}[4]{Style.RESET_ALL} ▸ ACTUALIZAR SNAPSHOT   [{Fore.YELLOW}⟳{Style.RESET_ALL}]                         ║
║  {Fore.RED}[5]{Style.RESET_ALL} ▸ SALIR DEL SISTEMA       [{Fore.RED}✖{Style.RESET_ALL}]                       ║
╠══════════════════════════════════════════════════════════╣
║  {Fore.YELLOW}▸ SELECCIONA TU OPCIÓN:{Style.RESET_ALL} """, end="")
        opcion = input(f"{Fore.CYAN}▸{Style.RESET_ALL} ")
        
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        if opcion == "1":
            print(f"{Fore.GREEN}[▓] INICIANDO PROTOCOLO...{Style.RESET_ALL}")
            iniciar()
        elif opcion == "2":
            print(f"{Fore.CYAN}[▓] ABRIENDO CANAL DE COMUNICACIÓN...{Style.RESET_ALL}")
            abrir_shell()
        elif opcion == "3":
            print(f"{Fore.MAGENTA}[▓] DETENIENDO SERVICIOS...{Style.RESET_ALL}")
            detener()
        elif opcion == "4":
            print(f"{Fore.YELLOW}[▓] ACTUALIZANDO SISTEMA Y GUARDANDO SNAPSHOT...{Style.RESET_ALL}")
            actualizar()
        elif opcion == "5":
            print(f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════╗
║  > CERRANDO SESIÓN...                                    ║
║  > CONEXIÓN TERMINADA                                    ║
║  > HASTA LA PRÓXIMA, HACKER                              ║
╚══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")
            break
        else:
            print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
            print(f"║  █ ERROR: OPCIÓN INVÁLIDA                                 ║")
            print(f"║  █ REINTENTA CON UN COMANDO VÁLIDO                       ║")
            print(f"╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()

if __name__ == "__main__":
    menu()
