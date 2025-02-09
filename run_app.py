import logging
import time
from threading import Thread
from config import edit_config, create_default_config
from database import init_db, clear_db, add_sms_data
from excel import read_from_excel
from sms_sender import send_sms
from server import start_server

logger = logging.getLogger('app_logger')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='w'
)

def run_sms_sender():

    time.sleep(8) # время на запуск сервера

    logger.info("Программа запущенна")

    # Создание (если нет) и редактирование файла конфигурации
    create_default_config()

    edit_config_input = input("Изменить конфигурационные данные? [y/n]: ").strip().lower()
    if edit_config_input in ("y","yes"):
        edit_config()

    # Путь до файла с данными
    file_path = input("Введите путь до файла (Файл - Скопировать как путь): ").replace('"', '')
    #file_path = "numbers.xlsx"

    # Считываем данные из таблицы
    df = read_from_excel(file_path)
    if not df:
        print("Не удалось прочитать данные из файла.")
        return
    
    # Создаем БД
    init_db()

    # Вопрос, нужно ли очистить базу данных
    clear_db_input = input("Очистить БД от предыдущих записей? [y/n]: ").strip().lower()
    if clear_db_input in ("y","yes"):
        clear_db()

    # Делаем рассылку для каждого номера из таблицы
    for phone_number, message in df.items():
        logger.info(f"Отправка SMS на номер {phone_number}...")
        add_sms_data(phone_number, message)
        send_sms(message, ['+' + str(phone_number)])

    logger.info(f"Рассылка завершена")

if __name__ == "__main__":
    server_thread = Thread(target=start_server, daemon=True)

    server_thread.start()

    # Запускаем основную логику
    run_sms_sender()

    # Ожидаем завершения потока сервера, если нужно
    server_thread.join()