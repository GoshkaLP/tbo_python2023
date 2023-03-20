from abc import ABC, abstractmethod


class NetworkAdapter(ABC):
    # Общий интерфейс для адаптеров
    @abstractmethod
    def ping(self, address: str) -> list:
        pass

    @abstractmethod
    def get_rtt(self, address: str) -> int | None:
        pass

    @abstractmethod
    def resolve_domain(self, domain: str) -> list:
        pass

    @abstractmethod
    def check_ports(self, address: str, ports: list) -> list:
        pass
