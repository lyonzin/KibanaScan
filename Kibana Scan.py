# --------------------------------------------------------------
#                 Kibana/Elastic Network Scanner
# 
# Descrição:
# Este script realiza uma varredura em blocos de endereços IP
# definidos pelo usuário, verificando se há portas abertas que 
# correspondem a serviços Kibana ou Elastic. Ao identificar uma
# porta aberta, o script tenta acessar o serviço via HTTP e
# valida se ele está operacional, registrando as URLs dos 
# serviços encontrados.
#
# Funcionalidades:
# - Varre blocos de IPs para verificar portas específicas.
# - Valida a presença de serviços Kibana/Elastic via HTTP.
# - Exibe um resumo dos resultados, incluindo o total de IPs 
#   verificados e URLs dos serviços encontrados.
# - Utiliza múltiplas threads para melhorar a performance 
#   da varredura.
#
# Configurações:
# - Blocos de IPs: Configuráveis pelo usuário.
# - Portas: Definidas para verificar serviços específicos.
# - Número de threads: Ajustável para controlar o paralelismo.
#
# Créditos:
# Ailton Rocha
# --------------------------------------------------------------

import socket
import requests
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from colorama import init, Fore, Style
import logging
from datetime import datetime
from tqdm import tqdm

# Configura o colorama
init(autoreset=True)

# Configura o logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Configurações
blocks_of_ips = [
    ip_network("10.0.0.0/8"),  # Exemplo de bloco /16
    ]
ports = [30333]
thread_count = 150  # Aumentar o número de threads para maior paralelismo

# Inicializações globais
total_ips_verificados = 0
total_servicos_encontrados = 0
urls_encontradas = []
portas_abertas = []

# Função para verificar se a porta está aberta
def is_port_open(ip, port):
    try:
        with socket.create_connection((str(ip), port), timeout=2):
            return True
    except (socket.error, socket.timeout):
        return False

# Função para validar se o Kibana está acessível via HTTP
def test_kibana_http(ip, port):
    url = f"http://{ip}:{port}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and ("Kibana" in response.text or "Elastic" in response.text):
            return url
    except requests.RequestException:
        pass
    return None

# Função principal de varredura para um único IP
def scan_ip(ip):
    global total_servicos_encontrados, urls_encontradas, portas_abertas
    ports_found = []
    for port in ports:
        if is_port_open(ip, port):
            ports_found.append(port)
            url = test_kibana_http(ip, port)
            if url:
                total_servicos_encontrados += 1
                urls_encontradas.append(url)

    if ports_found:
        portas_abertas.append((ip, ports_found))
    return ip

# Função para exibir o banner e informações adicionais
def display_banner(start_time):
    banner = r"""
     _____ _   _ ____  _____    _  _____  
    |_   _| | | |  _ \| ____|  / \|_   _|
      | | | |_| | |_) |  _|   / _ \ | |  
      | | |  _  |  _ <| |___ / ___ \| |  
      |_| |_| |_|_| \_\_____/_/   \_\_|  
 _   _ _   _ _   _ _____ ___ _   _  ____   _
| | | | | | | \ | |_   _|_ _| \ | |/ ___| | |
| |_| | | | |  \| | | |  | ||  \| | |  _  | |
|  _  | |_| | |\  | | |  | || |\  | |_| | |_|
|_| |_|\___/|_| \_| |_| |___|_| \_|\____| (_) 
"""
    print(Fore.CYAN + banner)
    print(Fore.CYAN + "       Kibana/Elastic Network Scanner        ")
    print(Fore.CYAN + "          ThreatHunting Detection           ")
    print(Fore.CYAN + "           Criador: Ailton Rocha           \n" + Style.RESET_ALL)
    print("-----------------------------------------------")
    print(f"{Fore.YELLOW}[+] Data e Hora de Início: {start_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[+] Redes a serem escaneadas: {', '.join([str(block) for block in blocks_of_ips])}{Style.RESET_ALL}")
    print("-----------------------------------------------")
    print("")

# Função principal para varrer os blocos de IPs
def scan_networks():
    global total_ips_verificados

    # Inicializa o contador de IPs
    total_ips = sum(1 for block in blocks_of_ips for _ in block.hosts())
    with tqdm(total=total_ips, ncols=100, bar_format="{l_bar}{bar} | IPs Verificados: {n_fmt}/{total_fmt}") as pbar:
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            future_to_ip = {executor.submit(scan_ip, ip): ip for block in blocks_of_ips for ip in block.hosts()}
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                pbar.set_description(f"{ip}")
                pbar.update(1)
                total_ips_verificados += 1

# Exibe o banner e inicia a varredura
start_time = datetime.now()
display_banner(start_time)
scan_networks()

# (DESATIVADO TEMPORARIAMENTE PRECISO AJUSTAR By Ailton)
# Exibe as portas abertas de maneira ordenada
#for ip, ports in portas_abertas:
#    tqdm.write(f"{Fore.GREEN}Portas abertas em {ip}: {ports}{Style.RESET_ALL}")

# Exibe o horário de término e o resumo dos resultados
end_time = datetime.now()
print("\n" + Fore.CYAN + "="*50 + Style.RESET_ALL)
print(f"{Fore.CYAN}Resumo da Varredura:{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Total de IPs Verificados: {total_ips_verificados}{Style.RESET_ALL}")
print(f"{Fore.GREEN}Total de Serviços Kibana/Elastic Encontrados: {total_servicos_encontrados}{Style.RESET_ALL}")

# Lista as URLs encontradas
if urls_encontradas:
    print(f"{Fore.GREEN}URLs encontradas:{Style.RESET_ALL}")
    for url in urls_encontradas:
        print(f" ⤷ {Fore.RED}{url}{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Nenhum serviço Kibana/Elastic encontrado.{Style.RESET_ALL}")

print(f"{Fore.YELLOW}Data e Hora de Término: {end_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
print(Fore.CYAN + "="*50 + Style.RESET_ALL)
logging.info("Varredura completa.")
