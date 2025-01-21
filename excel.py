import pandas as pd
import logging

logger = logging.getLogger('app_logger')

def read_from_excel(path: str):

    '''Функция считывает указанные столбцы и возвращает словарь (номер: сообщение).
    Функция делает проверку на наличие дубликатов и недопустимых символов.'''

    try: 

        logger.info(f"Попытка открыть excel файл: {path}")

        # Открытие файла Excel
        df = pd.read_excel(path)
        logger.info(f"Файл excel успешно открыт")

         # Проверка: столбцы "Номер" и "Порт" должны содержать только числа
        if not df['Номер'].apply(str).str.isdigit().all():
            logger.warning("Некоторые значения в столбце 'Номер' содержат недопустимые символы.")
            raise ValueError("Некоторые значения в столбце 'Номер' содержат недопустимые символы.")
        
        if not df['Порт'].apply(str).str.isdigit().all():
            logger.warning("Некоторые значения в столбце 'Порт' содержат недопустимые символы.")
            raise ValueError("Некоторые значения в столбце 'Порт' содержат недопустимые символы.")

        # Проверка на наличие дубликатов
        if df['Номер'].duplicated().any():
            logger.warning("Обнаружены дублирующиеся значения в столбце 'Номер'.")
            raise ValueError("В столбце 'Номер' обнаружены дублирующиеся значения.")
        
        if df['Порт'].duplicated().any():
            logger.warning("Обнаружены дублирующиеся значения в столбце 'Порт'.")
            raise ValueError("В столбце 'Порт' обнаружены дублирующиеся значения.")

        # Если в таблице нет сообщения (для меркурия) то генерируем его
        if 'Сообщение' not in df.columns:
            logger.info("Столбец 'Сообщение' отсутствует. Генерация сообщений...")
            # Генерируем сообщение
            df['Сообщение'] = df['Порт'].apply(
                lambda port: f"###111111!1!21!2!10.112.22.200!{port}!1!incotex!mts!mts!energytool.sib!0,0!"
            )
            logger.info("Сообщения успешно созданы")

        logger.info("Данные в файле excel успешно проверены и обработаны")
        print(df.head())  # Для отладки

        # Преобразование в словарь
        result = dict(zip(df['Номер'], df['Сообщение']))
        logger.info(f"Создан словарь значений: {len(result)} записей")
        return result

    except ValueError as ve:
        logger.error(f"Ошибка проверки данных: {ve}")
        return {}
    except FileNotFoundError:
        logger.critical(f"Файл не найден: {path}")
        return {}
    except Exception as e:
        logger.critical(f"Неизвестная ошибка: {e}")
        return {}