from .network_adapter import NetworkAdapter
from .ping_adapter import PingAdapter
from .socket_adapter import SocketAdapter

adapter = NetworkAdapter(PingAdapter(), SocketAdapter())
