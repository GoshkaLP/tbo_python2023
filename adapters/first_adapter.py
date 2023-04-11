import pythonping
import socket
import ssl
import certifi
from .network_adapter import NetworkAdapter


class FirstAdapter(NetworkAdapter):
    #  Реализация интерфейса NetworkAdapter с использованием библиотек pythonping и socket
    def ping(self, ip: str, count: int = 4) -> int:
        try:
            response = pythonping.ping(ip, count)
            packet_loss = response.packet_loss
            return packet_loss
        except Exception:
            return 100

    def get_rtt(self, address: str) -> int | None:
        try:
            response = pythonping.ping(address, count=1)
            return response.rtt_avg_ms
        except Exception as e:
            print(f"Ошибка получения RTT для {address}: {e}")
            return None

    def check_ports(self, address: str, ports: list) -> list:
        open_ports = []
        for port in ports:
            try:
                with socket.create_connection((address, port), timeout=5) as sock:
                    open_ports.append(port)
            except Exception as e:
                print(f"Ошибка проверки порта {port} для {address}: {e}")
        return open_ports

    def resolve_domain(self, domain: str) -> list:
        try:
            ips = socket.getaddrinfo(domain, None)
            return [ip[4][0] for ip in ips]
        except Exception as e:
            print(f"Ошибка разрешения доменного имени {domain}: {e}")
            return []

    def check_certificate(self, address: str) -> str:
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            with context.wrap_socket(socket.socket(), server_hostname=address) as s:
                s.connect((address, 443))
                s.getpeercert()
                return "valid cert"
        except ssl.SSLError as e:
            print(f"Ошибка проверки сертификата для {address}: {e}")
            return "INVALID cert"
