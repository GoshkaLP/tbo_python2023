from .ping_adapter import PingAdapter
from .socket_adapter import SocketAdapter


class NetworkAdapter:
    def __init__(self, ping_adapter: PingAdapter, socket_adapter: SocketAdapter):
        self.ping_adapter = ping_adapter
        self.socket_adapter = socket_adapter

    def ping(self, host: str, count: int = 4) -> int:
        return self.ping_adapter.ping(host, count)

    def get_rtt(self, host: str) -> int | None:
        return self.ping_adapter.get_rtt(host)

    def check_ports(self, host: str, ports: list) -> list:
        return self.socket_adapter.check_ports(host, ports)

    def resolve_domain(self, domain: str) -> list:
        return self.socket_adapter.resolve_domain(domain)
