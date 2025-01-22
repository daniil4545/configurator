import requests
import logging
from config import load_config

logger = logging.getLogger('app_logger')

def received_webhook(public_url):
    """Регистрирует вебхук (статус получения) на публичный URL ngrok."""
    # Загружаем конфигурацию из файла .env

    logger.info("Регистрация вэбхука")
    server, local_ip, username, password = load_config()

    # Формируем URL и данные для вебхука
    logger.info("Формирование POST запроса для регистрации вэбхука")
    webhook_url = f"{public_url}/sms" #куда слать вэбхуки
    url = "http://" + local_ip + "/webhooks" if server.lower() == "local" else "https://api.sms-gate.app/3rdparty/v1/webhooks" #откуда шлются вэбхуки

    data = {
        "id": "",
        "url": webhook_url,
        "event": "sms:received"
    }

    logger.info("POST запрос сформирован")

    try:
        # Выполняем POST-запрос для регистрации вебхука
        response = requests.post(url, json=data, auth=(username, password))
        if response.status_code == 200 or response.status_code == 201:
            logger.info(f"Вебхук успешно зарегистрирован на {webhook_url}")
            return True
        else:
            logger.error(f"Ошибка при регистрации вебхука: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        logger.error(f"Ошибка сети: {e}")
        return False
    
    
def delivered_webhook(public_url):
    """Регистрирует вебхук (статус доставки) на публичный URL ngrok."""
    # Загружаем конфигурацию из файла .env
    logger.info("Регистрация вэбхука")
    server, local_ip, username, password = load_config()

    # Формируем URL и данные для вебхука
    logger.info("Формирование POST запроса для регистрации вэбхука")
    webhook_url = f"{public_url}/sms" #куда слать вэбхуки
    url = "http://" + local_ip + "/webhooks" if server.lower() == "local" else "https://api.sms-gate.app/3rdparty/v1/webhooks" #откуда шлются вэбхуки

    data = {
        "id": "",
        "url": webhook_url,
        "event": "sms:delivered"
    }

    logger.info("POST запрос сформирован")

    try:
        # Выполняем POST-запрос для регистрации вебхука
        response = requests.post(url, json=data, auth=(username, password))
        if response.status_code == 200 or response.status_code == 201:
            logger.info(f"Вебхук успешно зарегистрирован на {webhook_url}")
            return True
        else:
            logger.error(f"Ошибка при регистрации вебхука: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        logger.error(f"Ошибка сети: {e}")
        return False