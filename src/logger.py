"""
Модуль логирования расчетов букета цветов.

Содержит функции для:
- записи результатов расчетов в файл
- чтения истории расчетов
- очистки логов
- форматирования записей

Формат лога:
[2026-03-26 14:30:15] РАСЧЕТ #1
  Цветы: Розы (15 шт) - 2250.00 руб
  Упаковка: Бумага - 100.00 руб
  Услуги: Доставка - 300.00 руб
  Скидка: 0.00 руб (0%)
  ИТОГО: 2650.00 руб

Author: [Твое имя]
Date: 2026-03-26
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# Настройки логирования
LOG_FILE = "bouquet_calculations.log"
LOG_ENCODING = "utf-8"
MAX_LOG_SIZE_BYTES = 1024 * 1024  # 1 MB
LOG_BACKUP_COUNT = 3


class BouquetLogger:
    """
    Класс для логирования расчетов букетов.

    Attributes:
        log_file (str): Путь к файлу лога
        calculation_counter (int): Счетчик расчетов в текущей сессии
    """

    def __init__(self, log_file: str = LOG_FILE):
        """
        Инициализация логгера.

        Args:
            log_file (str): Путь к файлу лога
        """
        self.log_file = log_file
        self.calculation_counter = self._get_last_calculation_number()

        # Создаем папку для логов, если нужно
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def _get_last_calculation_number(self) -> int:
        """
        Определяет номер последнего расчета из лога.

        Returns:
            int: Номер последнего расчета (0 если лога нет)
        """
        if not os.path.exists(self.log_file):
            return 0

        try:
            with open(self.log_file, 'r', encoding=LOG_ENCODING) as f:
                content = f.read()
                # Ищем последний номер расчета
                import re
                matches = re.findall(r'РАСЧЕТ #(\d+)', content)
                if matches:
                    return int(matches[-1])
        except Exception:
            pass

        return 0

    def _check_rotate_log(self):
        """
        Проверяет размер лога и создает резервную копию при превышении.
        """
        if not os.path.exists(self.log_file):
            return

        file_size = os.path.getsize(self.log_file)
        if file_size > MAX_LOG_SIZE_BYTES:
            # Создаем резервные копии
            for i in range(LOG_BACKUP_COUNT - 1, 0, -1):
                old_file = f"{self.log_file}.{i}"
                new_file = f"{self.log_file}.{i + 1}"
                if os.path.exists(old_file):
                    os.rename(old_file, new_file)

            # Перемещаем текущий лог
            if os.path.exists(self.log_file):
                os.rename(self.log_file, f"{self.log_file}.1")

    def _get_timestamp(self) -> str:
        """
        Возвращает текущую временную метку.

        Returns:
            str: Временная метка в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_calculation(self, user_data: Dict, result_data: Dict) -> bool:
        """
        Записывает результат расчета в лог-файл.

        Args:
            user_data (dict): Данные пользователя (цветы, количество и т.д.)
            result_data (dict): Результаты расчета (цены, скидка, итого)

        Returns:
            bool: True если запись успешна, False если ошибка
        """
        try:
            self._check_rotate_log()
            self.calculation_counter += 1

            # Форматируем запись
            log_entry = self._format_log_entry(user_data, result_data)

            # Записываем в файл
            with open(self.log_file, 'a', encoding=LOG_ENCODING) as f:
                f.write(log_entry)
                f.write("\n" + "=" * 60 + "\n\n")

            return True

        except Exception as e:
            print(f"Ошибка при записи в лог: {e}")
            return False

    def _format_log_entry(self, user_data: Dict, result_data: Dict) -> str:
        """
        Форматирует запись для лога.

        Args:
            user_data (dict): Данные пользователя
            result_data (dict): Результаты расчета

        Returns:
            str: Отформатированная строка для лога
        """
        # Преобразуем коды в названия
        flower_names = {1: "Розы", 2: "Тюльпаны", 3: "Хризантемы"}
        packaging_names = {1: "Лента", 2: "Бумага", 3: "Корзина"}

        # ========== ИСПРАВЛЕНИЕ №1: Безопасное получение flower_type ==========
        flower_type = user_data.get('flower_type', 1)
        flower_name = flower_names.get(flower_type, "Неизвестно")

        # ========== ИСПРАВЛЕНИЕ №2: Безопасное получение packaging ==========
        packaging_type = user_data.get('packaging', 1)
        packaging_name = packaging_names.get(packaging_type, "Неизвестно")

        # ========== ИСПРАВЛЕНИЕ №3: Безопасное получение quantity ==========
        quantity = user_data.get('quantity', 0)

        # Формируем список услуг
        services = []
        if user_data.get('delivery'):
            services.append("Доставка")
        if user_data.get('card'):
            services.append("Открытка")
        if user_data.get('self_pickup'):
            services.append("Самовывоз")

        services_str = ", ".join(services) if services else "Нет"

        # ========== ИСПРАВЛЕНИЕ №4: Безопасное получение цен ==========
        base_cost = result_data.get('base_cost', 0)
        packaging_cost = result_data.get('packaging_cost', 0)
        services_cost = result_data.get('services_cost', 0)
        discount = result_data.get('discount', 0)
        total_cost = result_data.get('total_cost', 0)

        # Расчет промежуточной суммы
        subtotal = result_data.get('subtotal', base_cost + packaging_cost + services_cost)

        # Расчет процента скидки
        discount_rate = 0
        if subtotal > 0:
            discount_rate = (discount / subtotal) * 100

        # Формируем запись
        timestamp = self._get_timestamp()
        entry = f"""
[{timestamp}] РАСЧЕТ #{self.calculation_counter}
--------------------------------------------------------------------------------
  Дата и время: {timestamp}

  СОСТАВ БУКЕТА:
    • Цветы: {flower_name} - {quantity} шт
    • Упаковка: {packaging_name}
    • Услуги: {services_str}

  СТОИМОСТЬ:
    • Цветы: {base_cost:.2f} руб
    • Упаковка: {packaging_cost:.2f} руб
    • Услуги: {services_cost:.2f} руб
    • Промежуточная сумма: {subtotal:.2f} руб
    • Скидка: -{discount:.2f} руб ({discount_rate:.1f}%)

  ИТОГОВАЯ СТОИМОСТЬ: {total_cost:.2f} руб
--------------------------------------------------------------------------------"""
        return entry

    def get_history(self, limit: Optional[int] = None) -> List[str]:
        """
        Возвращает историю расчетов из лога.

        Args:
            limit (int, optional): Максимальное количество записей

        Returns:
            list: Список строк с историей расчетов
        """
        if not os.path.exists(self.log_file):
            return []

        try:
            with open(self.log_file, 'r', encoding=LOG_ENCODING) as f:
                content = f.read()

            # Разделяем записи по разделителю
            entries = content.split("=" * 60)

            # Убираем пустые строки и очищаем
            entries = [e.strip() for e in entries if e.strip()]

            # Ограничиваем количество
            if limit and limit > 0:
                entries = entries[-limit:]

            return entries

        except Exception as e:
            print(f"Ошибка при чтении лога: {e}")
            return []

    def get_last_calculation(self) -> Optional[str]:
        """
        Возвращает последний расчет из лога.

        Returns:
            str или None: Последняя запись или None
        """
        history = self.get_history(limit=1)
        return history[0] if history else None

    def clear_log(self) -> bool:
        """
        Очищает файл лога.

        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            with open(self.log_file, 'w', encoding=LOG_ENCODING) as f:
                f.write("")
            self.calculation_counter = 0
            return True
        except Exception as e:
            print(f"Ошибка при очистке лога: {e}")
            return False

    def get_log_size(self) -> int:
        """
        Возвращает размер файла лога в байтах.

        Returns:
            int: Размер файла или 0 если файла нет
        """
        if os.path.exists(self.log_file):
            return os.path.getsize(self.log_file)
        return 0

    def get_log_path(self) -> str:
        """
        Возвращает полный путь к файлу лога.

        Returns:
            str: Путь к файлу лога
        """
        return os.path.abspath(self.log_file)

    def log_error(self, error_message: str, context: Optional[Dict] = None) -> bool:
        """
        Записывает ошибку в лог.

        Args:
            error_message (str): Сообщение об ошибке
            context (dict, optional): Дополнительный контекст

        Returns:
            bool: True если успешно
        """
        try:
            timestamp = self._get_timestamp()
            entry = f"""
[{timestamp}] ОШИБКА
--------------------------------------------------------------------------------
  {error_message}
"""
            if context:
                entry += f"  Контекст: {json.dumps(context, ensure_ascii=False)}\n"
            entry += "--------------------------------------------------------------------------------\n\n"

            with open(self.log_file, 'a', encoding=LOG_ENCODING) as f:
                f.write(entry)

            return True
        except Exception as e:
            print(f"Ошибка при записи ошибки в лог: {e}")
            return False

    def log_info(self, message: str) -> bool:
        """
        Записывает информационное сообщение в лог.

        Args:
            message (str): Сообщение для записи

        Returns:
            bool: True если успешно
        """
        try:
            timestamp = self._get_timestamp()
            entry = f"[{timestamp}] INFO: {message}\n\n"

            with open(self.log_file, 'a', encoding=LOG_ENCODING) as f:
                f.write(entry)

            return True
        except Exception as e:
            print(f"Ошибка при записи информации в лог: {e}")
            return False


# Создаем глобальный экземпляр логгера
_logger = None


def get_logger() -> BouquetLogger:
    """
    Возвращает глобальный экземпляр логгера (синглтон).

    Returns:
        BouquetLogger: Экземпляр логгера
    """
    global _logger
    if _logger is None:
        _logger = BouquetLogger()
    return _logger


# Упрощенные функции для обратной совместимости
def log_calculation(user_data: Dict, result_data: Dict) -> bool:
    """
    Упрощенная функция для записи расчета в лог.

    Args:
        user_data (dict): Данные пользователя
        result_data (dict): Результаты расчета

    Returns:
        bool: True если успешно
    """
    return get_logger().log_calculation(user_data, result_data)


def log_error(error_message: str, context: Optional[Dict] = None) -> bool:
    """
    Упрощенная функция для записи ошибки в лог.

    Args:
        error_message (str): Сообщение об ошибке
        context (dict, optional): Контекст ошибки

    Returns:
        bool: True если успешно
    """
    return get_logger().log_error(error_message, context)


def log_info(message: str) -> bool:
    """
    Упрощенная функция для записи информации в лог.

    Args:
        message (str): Сообщение

    Returns:
        bool: True если успешно
    """
    return get_logger().log_info(message)


def get_log_path() -> str:
    """Возвращает путь к файлу лога."""
    return get_logger().get_log_path()


def get_history(limit: Optional[int] = None) -> List[str]:
    """Возвращает историю расчетов."""
    return get_logger().get_history(limit)


def clear_log() -> bool:
    """Очищает лог."""
    return get_logger().clear_log()