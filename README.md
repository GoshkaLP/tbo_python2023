## TBO Network Monitor
Network Monitor - это небольшой инструмент для мониторинга состояния серверов и портов. 
Он проверяет доступность серверов, среднее время задержки RTT, состояние портов на серверах и валидность сертификата у Веб-серверов.  
В проекте используется паттерн Адаптер для обеспечения гибкости и возможности использовать различные реализации мониторинга сети.

### Структура проекта
project/  
│  
├── adapters/  
│   ├── __init__.py  
│   ├── network_adapter.py  
│   └── first_adapter.py  
│  
├── monitor.py  
├── config.py  
├── config.csv  
└── main.py  
### Установка
1. Установите необходимые зависимости:  
```pip install pythonping```

2. Склонируйте репозиторий:
```
git clone https://github.com/GoshkaLP/tbo_python2023.git
cd tbo_python2023
```
3. Отредактируйте файл config.csv, добавив хосты и порты, которые вы хотите отслеживать.
### Запуск  
Запустите main.py:  
```python main.py```  
Программа начнет мониторить сервера и порты, указанные в config.csv, и выводить результаты в консоль.

### Настройка
Файл config.csv содержит список серверов и портов для мониторинга.   
Структура файла следующая:
```
Host;Ports
example.com;80,443
192.168.1.1;22
localhost;
```
Первая строка заголовка и не должна быть изменена.  
Каждая последующая строка содержит имя хоста или IP-адрес и список портов, разделенных запятыми.  
Если необходимо проверить только доступность сервера, без проверки портов, оставьте поле портов пустым.  

### Кастомизация
Вы можете добавить свою реализацию адаптера для мониторинга сети. 
Просто создайте новый файл в каталоге `adapters` и наследуйте ваш класс от `NetworkAdapter`.   
Затем имплементируйте методы `ping`, `get_rtt`, `resolve_domain`, и `check_ports` согласно вашим потребностям. 
После этого импортируйте и используйте ваш новый адаптер в `monitor.py`.

### Авторство
[Рыбкин Георгий](https://gmrybkin.com), 2023