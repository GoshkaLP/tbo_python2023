from datetime import datetime
from adapters import NetworkAdapter
import time
import re


class ServerMonitor:
    def __init__(self, config_file: list, network_adapter: NetworkAdapter):
        self.config = config_file
        self.network_adapter = network_adapter

    @staticmethod
    def is_host_ip(host: str) -> bool:
        # Проверка, является ли переданный хост IP-адресом
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, host):
            octets = host.split('.')
            if all(int(octet) < 256 for octet in octets):
                return True
        return False

    @staticmethod
    def is_valid_host(host: str) -> bool:
        # Проверка, является ли переданный хост допустимым IP-адресом или доменным именем
        hostname_pattern = r'^[a-zA-Z0-9]+([\-.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,20}$'
        special_domains = ['localhost', 'broadcasthost']

        if host in special_domains:
            return True

        if ServerMonitor.is_host_ip(host):
            return True

        if re.match(hostname_pattern, host):
            return True

        return False

    @staticmethod
    def validate_input_data(input_data: list) -> bool:
        # Валидация данных входного файла
        validation_result = True
        for row_number, entry in enumerate(input_data, 2):
            host, port_list = entry
            if ServerMonitor.is_valid_host(host):
                if not host and port_list:
                    print(f"Некорректные входные данные: отсутствует доменное имя. Строка {row_number}")
                if not host and not port_list:
                    print(f"Некорректные входные данные: и доменное имя, и порт отсутствуют. Строка {row_number}")
                    validation_result = False
                if port_list:
                    for port in port_list:
                        if not port.isdigit() or int(port) < 0 or int(port) > 65535:
                            print(f"Некорректные входные данные: недопустимый порт '{port}'. Строка {row_number}")
                            validation_result = False
            else:
                print(f"Некорректные входные данные: неверный IP-адрес '{host}'. Строка {row_number}")
                validation_result = False
        return validation_result

    def is_internet_available(self) -> bool:
        # Проверка доступности интернет-соединения
        internet_rtt_check = self.network_adapter.get_rtt('8.8.8.8')
        if internet_rtt_check is not None and internet_rtt_check < 2000:
            return True
        else:
            return False

    def monitor_server(self, host: str, ports: list) -> None:
        # Функция мониторинга сервера
        if not self.is_internet_available():
            print("Отсутсвует интернет-соединение. Ждем восстановление доступа.")
            while not self.is_internet_available():
                time.sleep(10)  # Check every 10 seconds
            print("Интернет-соединение восстановлено.\n")

        ips = list(set(self.network_adapter.resolve_domain(host))) if host else ['']
        if not host or self.is_host_ip(host):
            host = '???'
        print(f"['{host}', {ips}, {ports}]")
        for ip in ips:
            lost_packets = self.network_adapter.ping(ip)
            rtt = self.network_adapter.get_rtt(ip) if lost_packets != 100 else None
            open_ports = self.network_adapter.check_ports(ip, ports) if ports else []
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if not ports:
                print(f"{timestamp} | {host} | {ip} | {lost_packets} | {rtt} ms | -1 | ???")
            else:
                for port in ports:
                    status = 'Opened' if port in open_ports else 'Unknown'
                    if port == '443':
                        cert_status = self.network_adapter.check_certificate(host if host != '???' else ip)
                        print(f"{timestamp} | {host} | {ip} | {lost_packets} | {rtt} ms | {port} | {status} "
                              f"| {cert_status}")
                    else:
                        print(f"{timestamp} | {host} | {ip} | {lost_packets} | {rtt} ms | {port} | {status}")
        print()

    def monitor(self) -> None:
        # Функция мониторинга всех серверов из файла конфигурации
        for host, ports in self.config:
            self.monitor_server(host, ports)
