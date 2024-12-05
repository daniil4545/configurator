import sqlite3
from datetime import datetime

# Инициализация БД
def init_db():
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sms_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT,
        message TEXT,
        response_message TEXT,
        response_timestamp TEXT
    )''')
    conn.commit()
    conn.close()

# Очистка БД
def clear_db():
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS sms_data")
    init_db()
    conn.close()
    print("База данных очищенна")

# Добавление номеров и отосланых СМС
def add_sms_data(phone_number, message):
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sms_data (phone_number, message) VALUES (?, ?)",
                   (phone_number, message))
    conn.commit()
    conn.close()

# Обновление БД при получении ответного СМС
def update_response(phone_number, response_message, time):
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE sms_data SET response_message = ?, response_timestamp = ? WHERE phone_number = ?",
                   (response_message, time, phone_number))
    conn.commit()
    conn.close()
    print("Данные в БД обновлены.")

# Запрос всех значений из БД
def get_all_messages():
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sms_data")
    messages = cursor.fetchall()
    conn.close()
    return messages