import time
from adapters import FirstAdapter

from config import read_config
from monitor import ServerMonitor


def main() -> None:
    input_data = read_config("config.csv")
    if not ServerMonitor.validate_input_data(input_data):
        print("Приложение остановлено из-за некорректных входных данных.")
        return
    # Здесь можем менять адаптер на любой другой, реализующий абстрактный класс NetworkAdapter
    adapter = FirstAdapter()
    monitor = ServerMonitor(input_data, adapter)
    while True:
        try:
            monitor.monitor()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)


if __name__ == '__main__':
    main()
