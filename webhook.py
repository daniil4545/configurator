import requests
import logging
from config import load_config

logger = logging.getLogger(__name__)

def register_webhook(public_url):
    """Регистрирует вебхук на публичный URL ngrok."""
    # Загружаем конфигурацию из файла .env
    logger.info("Регистрация вэбхука")
    username, password, server_adress = load_config()

    # Формируем URL и данные для вебхука
    logger.info("Формирование POST запроса для регистрации вэбхука")
    webhook_url = f"{public_url}/sms"
    api_url = "https://" + server_adress + "/webhooks"

    data = {
        "id": "",
        "url": webhook_url,
        "event": "sms:received"
    }

    logger.info("POST запрос сформирован")

    try:
        # Выполняем POST-запрос для регистрации вебхука
        response = requests.post(api_url, json=data, auth=(username, password))
        if response.status_code == 200 or response.status_code == 201:
            logger.info(f"Вебхук успешно зарегистрирован на {webhook_url}")
            return True
        else:
            logger.error(f"Ошибка при регистрации вебхука: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        logger.error(f"Ошибка сети: {e}")
        return False
