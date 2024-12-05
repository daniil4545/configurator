from database import update_response, get_all_messages
from multiprocessing import Process, Queue
from flask import Flask, request, render_template, jsonify
from pyngrok import ngrok
from webhook import register_webhook

app = Flask(__name__)
 
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

    print(f"SMS от {phone_number}: {message}")

    update_response(phone_number, message, time)

    return jsonify({"status": "received"}), 200


@app.route('/', methods=['GET'])
def list_sms():
    '''Старница с визуализацией данных из БД'''
    messages = get_all_messages()

    return render_template('sms_list.html', messages=messages)


def start_server(queue):
    """Функция запуска сервера Flask с ngrok."""

    # Запускаем ngrok для получения публичного адреса
    public_url = ngrok.connect(5000).public_url

    queue.put(public_url)

    # Запускаем локальный сервер для обработки веб-хуков
    app.run(host='0.0.0.0', port=5000)

def main():
    address_queue = Queue()

    # Запуск сервера
    server_process = Process(target=start_server, args=(address_queue,), daemon=True)
    server_process.start()

    # Получение публичного URL
    server_address = address_queue.get()

    print(f"\nСервер доступен по адресу: {server_address}")

    # Регестрируем вэб-хук на публичный адрес
    register_webhook(server_address)

    input("Нажмите Enter для завершения программы...")
    print("Программа завершена.")


if __name__ == "__main__":
    main()