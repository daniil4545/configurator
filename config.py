import os
from dotenv import load_dotenv, find_dotenv
import logging

logger = logging.getLogger('app_logger')

CONFIG_PATH = find_dotenv()

def create_default_config():
    """Создаёт конфигурационный файл с дефолтными значениями, если его нет."""
    logger.info("Проверка наличия файла конфигурации")
    if not os.path.exists(CONFIG_PATH):
        logging.info("Конфигурационный файл отсутствует. Создаём файл с начальными значениями")
        with open(CONFIG_PATH, 'w') as f:
            f.write("SERVER=local\n")
            f.write("LOCAL_ADDRESS=192.168.1.182:8080")
            f.write("GATEWAY_USERNAME=mts\n")
            f.write("PASSWORD=mtsmts123\n")
            f.close()
    logger.info("Файл конфигурации найден")

def edit_config():
    """Открывает конфигурационный файл."""
    logger.info("Открытие конфигурационного файла для редактирования")
    os.system(f'notepad {CONFIG_PATH}')
    logger.info("Конфигурационный файл изменен")

def load_config():
    """Загружает конфигурацию из файла."""
    logger.info("Выгрузка данных из файла конфигурации")
    load_dotenv(CONFIG_PATH)
    
    server = os.getenv("SERVER")
    local_ip = os.getenv("LOCAL_ADDRESS")
    username = os.getenv("GATEWAY_USERNAME")
    password = os.getenv("PASSWORD")

    return server, local_ip, username, password