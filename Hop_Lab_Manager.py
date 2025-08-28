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
    spin_chars = ['-', '\\', '|', '/']
    i = 0
    while proc.poll() is None:
        sys.stdout.write(f"\r{Fore.CYAN}[{spin_chars[i % 4]}]{Style.RESET_ALL} Procesando...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print(f"\r{Fore.GREEN}✔ Hecho!{Style.RESET_ALL}          ")

# Ejecutar comando con spinner
def run_cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    spin_thread = threading.Thread(target=spinner, args=(proc,))
    spin_thread.start()
    stdout, stderr = proc.communicate()
    spin_thread.join()
    return stdout.decode().strip(), stderr.decode().strip()

# Función para iniciar el contenedor
def iniciar():
    # Si ya existe, eliminarlo primero
    out, _ = run_cmd(f'{sudo_prefix}docker ps -a -q -f "name=^{CONTAINER_NAME}$"')
    if out:
        print(Fore.YELLOW + "El contenedor ya existe, eliminando...")
        run_cmd(f"{sudo_prefix}docker rm -f {CONTAINER_NAME}")

    # Crear y arrancar contenedor en segundo plano
    print(Fore.GREEN + "Iniciando contenedor...")
    current_dir = subprocess.getoutput("pwd") if not sys.platform.startswith("win") else subprocess.getoutput("cd")
    run_cmd([
        f"{sudo_prefix}docker run --network=host --privileged --name {CONTAINER_NAME} "
        f"-v {current_dir}:/home -d {IMAGE_NAME} tail -f /dev/null"
    ])
    print(Fore.GREEN + f"Contenedor {CONTAINER_NAME} iniciado correctamente.")

# Abrir shell interactivo en contenedor
def abrir_shell():
    # Comprueba si está corriendo
    out, _ = run_cmd(f'{sudo_prefix}docker ps -q -f "name=^{CONTAINER_NAME}$"')
    if not out:
        print(Fore.RED + "El contenedor no está en ejecución. Primero inicia el contenedor.")
        return
    shell_cmd = f"{sudo_prefix}docker exec -ti {CONTAINER_NAME} cmd" if sys.platform.startswith("win") else f"{sudo_prefix}docker exec -ti {CONTAINER_NAME} /bin/bash"
    subprocess.run(shell_cmd, shell=True)

# Detener contenedor
def detener():
    out, _ = run_cmd(f'{sudo_prefix}docker ps -q -f "name=^{CONTAINER_NAME}$"')
    if not out:
        print(Fore.YELLOW + "El contenedor ya está detenido.")
        return
    print(Fore.RED + "Deteniendo contenedor...")
    run_cmd(f"{sudo_prefix}docker stop {CONTAINER_NAME}")
    print(Fore.RED + "Contenedor detenido.")

# Menú
def menu():
    while True:
        print(Fore.BLUE + "==============================")
        print(Fore.GREEN + " BIENVENIDO AL MENU DEL LABO")
        print(Fore.YELLOW + " SELECCIONA QUE NECESITAS HACER ")
        print(Fore.BLUE + "==============================")
        print(Fore.GREEN + "1) Iniciar el Labo")
        print(Fore.CYAN + "2) Abrir un Shell")
        print(Fore.MAGENTA + "3) Detener el Labo")
        print(Fore.RED + "4) Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            iniciar()
        elif opcion == "2":
            abrir_shell()
        elif opcion == "3":
            detener()
        elif opcion == "4":
            print(Fore.RED + "Saliendo...")
            break
        else:
            print(Fore.RED + "Opción inválida, intenta de nuevo.")
        print()

if __name__ == "__main__":
    menu()
