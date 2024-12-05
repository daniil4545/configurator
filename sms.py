import requests
from config import load_config

def send_sms(message: str, phone_number):
    '''Функция отправки SMS'''
    # Получаем данные из файла окружения
    username, password, server_adress = load_config()

    # Формируем запрос к шлюзу
    url = f"http://{server_adress}/message"

    print(url)

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "message": message,
        "phoneNumbers": phone_number
    }
    
    # Делаем запрос к шклюзу
    try:
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth(username, password), headers=headers, json=data)
        response.raise_for_status()
    except Exception as err:
        print(f'Error: {err}')


    if response.status_code == 200 or response.status_code == 202:
        print(f'СМС успешно отправлено на номер {phone_number}')
    else:
        print(f'Ошибка при отправке СМС на номер {phone_number}: {response.status_code}')