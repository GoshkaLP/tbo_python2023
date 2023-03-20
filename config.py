import csv


def read_config(file_name: str) -> list:
    # Функция для чтения файла конфигурации
    config = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            host = row[0].strip()
            ports = [port.strip() for port in row[1].split(',') if port.strip()]
            config.append((host, ports))
    return config
