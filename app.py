from config import edit_config, create_default_config
from database import init_db, clear_db, add_sms_data, update_response, get_all_messages
from excel import read_from_excel
import subprocess
from sms import send_sms

def main():

    # Создание (если нет) и редактирование файла конфигурации
    create_default_config()

    edit_config_input = input("Изменить конфигурационные данные? [y/n]: ").strip().lower()
    if edit_config_input in ("y","yes","Y","YES","Yes"):
        edit_config()

    # Путь до файла с данными
    file_path = input("Введите путь до файла (Файл - Скопировать как путь): ").replace('"', '')

    # Считываем данные из таблицы
    df = read_from_excel(file_path)
    if not df:
        print("Не удалось прочитать данные из файла.")
        return
    
    # Создаем БД
    init_db()

    # Вопрос, нужно ли очистить базу данных
    clear_db_input = input("Очистить БД от предыдущих записей? [y/n]: ").strip().lower()
    if clear_db_input in ("y","yes","Y","YES","Yes"):
        clear_db()

    # Делаем рассылку для каждого номера из таблицы
    for phone_number, message in df.items():
        print(f"Отправка SMS на номер {phone_number}.")
        add_sms_data(phone_number, message)
        send_sms(message, ['+' + str(phone_number)])

    # Запуск сервера в отдельном процессе
    server_script = "server.py"
    subprocess.Popen(["python", server_script])

if __name__ == "__main__":
    main()