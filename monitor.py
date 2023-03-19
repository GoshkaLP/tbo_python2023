from datetime import datetime
from config import read_config
from ping_adapter import PingAdapter
from network_adapter import NetworkAdapter
import time


def is_internet_available(network_adapter: NetworkAdapter) -> bool:
    internet_rtt_check = network_adapter.get_rtt('8.8.8.8')
    if internet_rtt_check is not None and internet_rtt_check < 2000:
        return True
    else:
        return False


def monitor_server(network_adapter: NetworkAdapter, host: str, ports: list) -> None:
    if not is_internet_available(network_adapter):
        print("Отсутсвует интернет-соединение. Ждем восстановление доступа.")
        while not is_internet_available(network_adapter):
            time.sleep(10)  # Check every 10 seconds
        print("Интернет-соединение восстановлено.\n")

    ips = list(set(network_adapter.resolve_domain(host))) if host else ['']
    if not host:
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
    config = read_config(config_file)
    network_adapter = PingAdapter()

    for host, ports in config:
        monitor_server(network_adapter, host, ports)
