import time
import re

from config import read_config
from monitor import monitor


def is_valid_host(host: str) -> bool:
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    hostname_pattern = r'^[a-zA-Z0-9]+([\-.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,20}$'
    special_domains = ['localhost', 'broadcasthost']

    if host in special_domains:
        return True

    if re.match(ip_pattern, host):
        octets = host.split('.')
        if all(int(octet) < 256 for octet in octets):
            return True

    if re.match(hostname_pattern, host):
        return True

    return False


def validate_input_data(input_data: list) -> bool:
    validation_result = True
    for row_number, entry in enumerate(input_data, 2):
        host, port_list = entry
        if is_valid_host(host):
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


def main() -> None:
    input_data = read_config("config.csv")
    if not validate_input_data(input_data):
        print("Приложение остановлено из-за некорректных входных данных.")
        return

    while True:
        try:
            monitor('config.csv')
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)


if __name__ == '__main__':
    main()
