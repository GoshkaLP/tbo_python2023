import pythonping


class PingAdapter:
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
