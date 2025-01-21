import logging
from multiprocessing import Process, Queue
from flask import Flask, request, render_template, jsonify
from pyngrok import ngrok
from time import sleep

from webhook import received_webhook, delivered_webhook
from database import update_response, get_all_messages

app = Flask(__name__)

logger = logging.getLogger('app_logger')
 
@app.route('/sms', methods=['POST'])
def receive_sms():
    '''Прием и обработка вэб-хуков от SMS Gateway'''
    data = request.json

    payload = data.get("payload", {})
    phone_number = payload.get("phoneNumber")  # Получение номера телефона
    message = payload.get("message")  # Получение сообщения
    time = payload.get("receivedAt") # Получение метки времени

    # Удаление символа '+' из номера
    if str(phone_number).startswith('+'):
        phone_number = phone_number[1:]

    logger.info(f"SMS от {phone_number}: {message}")

    update_response(phone_number, message, time)

    return jsonify({"status": "received"}), 200


@app.route('/', methods=['GET'])
def list_sms():
    '''Страница с визуализацией данных из БД'''
    messages = get_all_messages()

    return render_template('sms_list.html', messages=messages)


def start_server():
    """Функция запуска сервера Flask с ngrok."""

    logger.info("Запуск ngrok, получение публичного url")

    # Запускаем ngrok для получения публичного адреса
    public_url = ngrok.connect(5000).public_url
    sleep(5)

    logger.info(f'Публичный адрес получен:{public_url}')
    print(f"\nСервер доступен по адресу: {public_url}")

    # Регистрируем вэбхуки
    received_webhook(public_url)

    # Запускаем локальный сервер для обработки веб-хуков
    logger.info('Запуск локального сервера')
    app.run(host='0.0.0.0', port=5000)