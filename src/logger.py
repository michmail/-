"""
Модуль логирования.
"""

import datetime
from typing import Dict

LOG_FILE = "delivery_log.txt"


def log_result(result: Dict) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"""
{'=' * 50}
Время: {timestamp}
Цветы: {result['flower_name']}, {result['quantity']} шт
Стоимость цветов: {result['base_cost']} руб
Упаковка: {result['packaging_name']} - {result['packaging_cost']} руб
Доставка: {'Да' if result['delivery'] else 'Нет'}
Открытка: {'Да' if result['card'] else 'Нет'}
Стоимость услуг: {result['services_cost']} руб
Итоговая стоимость: {result['total_cost']} руб
{'=' * 50}
"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    print(f"\nРезультат сохранён в файл {LOG_FILE}")