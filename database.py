import sqlite3
import logging

logger = logging.getLogger(__name__)

# Инициализация БД
def init_db():
    logger.info("Инициализация БД")
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
    logger.info("БД инициализированна")

# Очистка БД
def clear_db():
    logger.info("удаление текущей БД")
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS sms_data")
    init_db()
    conn.close()
    logging.info("БД очищенна")

# Добавление номеров и отосланых СМС
def add_sms_data(phone_number, message):
    logger.info(f"Добавление номера {phone_number} в БД")
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sms_data (phone_number, message) VALUES (?, ?)",
                   (phone_number, message))
    conn.commit()
    conn.close()
    logger.info(f"Номер {phone_number} добавлен в БД")

# Обновление БД при получении ответного СМС
def update_response(phone_number, response_message, time):
    logger.info("Обновление БД новыми значениями")
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE sms_data SET response_message = ?, response_timestamp = ? WHERE phone_number = ?",
                   (response_message, time, phone_number))
    conn.commit()
    conn.close()
    logging.info("Данные в БД обновлены")

# Запрос всех значений из БД
def get_all_messages():
    conn = sqlite3.connect('sms.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sms_data")
    messages = cursor.fetchall()
    conn.close()
    return messages