import os
from dotenv import load_dotenv

CONFIG_PATH = "configurator.env"

def create_default_config():
    """Создаёт конфигурационный файл с дефолтными значениями, если его нет."""
    if not os.path.exists(CONFIG_PATH):
        print("Конфигурационный файл отсутствует. Создаём файл с дефолтными значениями...")
        with open(CONFIG_PATH, 'w') as f:
            f.write("GATEWAY_USERNAME=P-KHRJ\n")
            f.write("PASSWORD=qbalabdocp6abd\n")
            f.write("SERVER_ADRESS=api.sms-gate.app/3rdparty/v1\n")
            f.close()

def edit_config():
    """Открывает конфигурационный файл."""
    print("Открытие конфигурационного файла для редактирования...")
    os.system(f'notepad {CONFIG_PATH}')

def load_config():
    """Загружает конфигурацию из файла."""
    load_dotenv(CONFIG_PATH)
    
    username = os.getenv("GATEWAY_USERNAME")
    password = os.getenv("PASSWORD")
    server_adress = os.getenv("SERVER_ADRESS")

    return username, password, server_adress