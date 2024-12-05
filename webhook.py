import requests
from config import load_config

def register_webhook(public_url):
    """Регистрирует вебхук на публичный URL ngrok."""
    # Загружаем конфигурацию из файла .env
    username, password, server_adress = load_config()

    # Формируем URL и данные для вебхука
    webhook_url = f"{public_url}/sms"
    api_url = "https://" + server_adress + "/webhooks"

    data = {
        "id": "",
        "url": webhook_url,
        "event": "sms:received"
    }

    try:
        # Выполняем POST-запрос для регистрации вебхука
        response = requests.post(api_url, json=data, auth=(username, password))
        if response.status_code == 200 or response.status_code == 201:
            print(f"Вебхук успешно зарегистрирован на {webhook_url}")
            return True
        else:
            print(f"Ошибка при регистрации вебхука: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
        return False
