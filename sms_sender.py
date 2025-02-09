import requests
import logging
from config import load_config

logger = logging.getLogger('app_logger')

def send_sms(message: str, phone_number):
    '''Функция отправки SMS'''

    logger.info("Вызов функции рассылки SMS")

    # Получаем данные из файла окружения
    server, local_ip, username, password = load_config()

    # Формируем запрос к шлюзу
    url = "http://" + local_ip + "/message" if server.lower() == "local" else "https://api.sms-gate.app/3rdparty/v1/message"

    logger.info(f"Адрес шлюза:{url}")

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "message": message,
        "phoneNumbers": phone_number
    }
    
    # Делаем запрос к шлюзу
    logger.info(f"Формирование запроса к шлюзу")
    try:
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth(username, password), headers=headers, json=data)
        response.raise_for_status()
        logger.info(f"Запрос отправлен на шлюз")
    except Exception as err:
        logger.error(f'Error: {err}')


    if response.status_code == 200 or response.status_code == 202:
        logger.info(f'СМС успешно отправлено на номер {phone_number}')
    else:
        logger.error(f'Ошибка при отправке СМС на номер {phone_number}: {response.status_code}')