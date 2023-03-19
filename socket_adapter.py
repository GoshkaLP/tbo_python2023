import socket
from network_adapter import NetworkAdapter


class SocketAdapter(NetworkAdapter):
    def ping(self, address: str) -> list:
        pass

    def get_rtt(self, address: str) -> int | None:
        pass

    def resolve_domain(self, domain: str) -> list:
        try:
            ips = socket.getaddrinfo(domain, None)
            return [ip[4][0] for ip in ips]
        except Exception as e:
            print(f"Ошибка разрешения доменного имени {domain}: {e}")
            return []

    def check_ports(self, address: str, ports: list) -> list:
        open_ports = []
        for port in ports:
            try:
                with socket.create_connection((address, port), timeout=5) as sock:
                    open_ports.append(port)
            except Exception as e:
                print(f"Ошибка проверки порта {port} для {address}: {e}")
        return open_ports
