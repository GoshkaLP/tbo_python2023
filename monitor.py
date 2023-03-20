from datetime import datetime
from config import read_config
from adapters import NetworkAdapter, FirstAdapter
import time

import re


def is_host_ip(host: str) -> bool:
    # Проверка, является ли переданный хост IP-адресом
    return re.match(r'^(\d{1,3}\.){3}\d{1,3}$', host) is not None


def is_internet_available(network_adapter: NetworkAdapter) -> bool:
    # Проверка доступности интернет-соединения
    internet_rtt_check = network_adapter.get_rtt('8.8.8.8')
    if internet_rtt_check is not None and internet_rtt_check < 2000:
        return True
    else:
        return False


def monitor_server(network_adapter: NetworkAdapter, host: str, ports: list) -> None:
    # Функция мониторинга сервера
    if not is_internet_available(network_adapter):
        print("Отсутсвует интернет-соединение. Ждем восстановление доступа.")
        while not is_internet_available(network_adapter):
            time.sleep(10)  # Check every 10 seconds
        print("Интернет-соединение восстановлено.\n")

    ips = list(set(network_adapter.resolve_domain(host))) if host else ['']
    if not host or is_host_ip(host):
        host = '???'
    print(f"['{host}', {ips}, {ports}]")
    for ip in ips:
        lost_packets = network_adapter.ping(ip)
        rtt = network_adapter.get_rtt(ip) if lost_packets != 100 else None
        open_ports = network_adapter.check_ports(ip, ports) if ports else []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if not ports:
            print(f"{timestamp} | {host} | {ip} | {lost_packets} | {rtt} ms | -1 | ???")
        else:
            for port in ports:
                status = 'Opened' if port in open_ports else 'Unknown'
                print(f"{timestamp} | {host} | {ip} | {lost_packets} | {rtt} ms | {port} | {status}")
    print()


def monitor(config_file: str) -> None:
    # Функция мониторинга всех серверов из файла конфигурации
    config = read_config(config_file)
    adapter = FirstAdapter()

    for host, ports in config:
        monitor_server(adapter, host, ports)
