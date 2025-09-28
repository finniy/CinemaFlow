import logging
from colorama import init, Fore, Style

# Инициализация colorama для корректного отображения цветов в терминале
init(autoreset=True)


class ColorFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        # Ошибки и критические — красным
        if record.levelno >= logging.ERROR:
            return Fore.RED + msg + Style.RESET_ALL
        # Инфо — зелёным
        elif record.levelno == logging.INFO:
            return Fore.GREEN + msg + Style.RESET_ALL
        # Для других уровней без цвета
        return msg


# Создаем логгер с именем твоего проекта
logger = logging.getLogger('ip_tracker_bot')
logger.setLevel(logging.DEBUG)  # можно поставить INFO, если не нужны debug сообщения

# Формат: дата, время, уровень лога, сообщение
formatter = ColorFormatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Обработчик вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Добавляем обработчик в логгер, если он еще не добавлен
if not logger.hasHandlers():
    logger.addHandler(console_handler)
