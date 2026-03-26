"""
Модуль ввода/вывода для калькулятора стоимости букета цветов.

Содержит функции для:
- безопасного ввода данных от пользователя
- запроса всех параметров букета
- отображения результатов расчета в удобном формате

Author: [Твое имя]
Date: 2026-03-26
"""

import sys


def safe_input_int(prompt, min_value=None, max_value=None):
    """
    Безопасный ввод целого числа с проверкой диапазона.

    Args:
        prompt (str): Приглашение к вводу
        min_value (int, optional): Минимальное допустимое значение
        max_value (int, optional): Максимальное допустимое значение

    Returns:
        int: Введенное пользователем число

    Raises:
        KeyboardInterrupt: При прерывании ввода (Ctrl+C)
    """
    while True:
        try:
            value = input(prompt).strip()

            # Проверка на пустой ввод
            if not value:
                print("Ошибка: ввод не может быть пустым")
                continue

            # Преобразование в целое число
            value = int(value)

            # Проверка минимального значения
            if min_value is not None and value < min_value:
                print(f"Ошибка: значение должно быть не меньше {min_value}")
                continue

            # Проверка максимального значения
            if max_value is not None and value > max_value:
                print(f"Ошибка: значение должно быть не больше {max_value}")
                continue

            return value

        except ValueError:
            print("Ошибка: введите целое число")
        except KeyboardInterrupt:
            print("\nВвод прерван пользователем")
            sys.exit(0)


def safe_input_bool(prompt, default=None):
    """
    Безопасный ввод булевого значения (да/нет).

    Args:
        prompt (str): Приглашение к вводу
        default (bool, optional): Значение по умолчанию, если пользователь нажмет Enter

    Returns:
        bool: True если пользователь ввел 'да', False если 'нет'
    """
    # Формируем подсказку с учетом значения по умолчанию
    if default is True:
        prompt = f"{prompt} (да/нет) [да]: "
    elif default is False:
        prompt = f"{prompt} (да/нет) [нет]: "
    else:
        prompt = f"{prompt} (да/нет): "

    while True:
        try:
            value = input(prompt).strip().lower()

            # Если пользователь нажал Enter и есть значение по умолчанию
            if not value and default is not None:
                return default

            # Проверка положительных ответов
            if value in ['да', 'yes', 'y', '1', 'true', '+', 'д']:
                return True

            # Проверка отрицательных ответов
            if value in ['нет', 'no', 'n', '0', 'false', '-', 'н']:
                return False

            print("Ошибка: введите 'да' или 'нет'")

        except KeyboardInterrupt:
            print("\nВвод прерван пользователем")
            sys.exit(0)


def get_flower_type():
    """
    Запрашивает выбор типа цветов.

    Returns:
        int: 1 - розы, 2 - тюльпаны, 3 - хризантемы
    """
    print("\n--- ВЫБОР ЦВЕТОВ ---")
    print("  1 - Розы (150 руб/шт)")
    print("  2 - Тюльпаны (80 руб/шт)")
    print("  3 - Хризантемы (100 руб/шт)")

    return safe_input_int("Ваш выбор (1-3): ", min_value=1, max_value=3)


def get_quantity():
    """
    Запрашивает количество цветов.

    Returns:
        int: Количество цветов (положительное целое число)
    """
    print("\n--- КОЛИЧЕСТВО ---")
    return safe_input_int("Количество цветов: ", min_value=1, max_value=1000)


def get_packaging_type():
    """
    Запрашивает выбор типа упаковки.

    Returns:
        int: 1 - лента, 2 - бумага, 3 - корзина
    """
    print("\n--- ВЫБОР УПАКОВКИ ---")
    print("  1 - Лента (50 руб)")
    print("  2 - Бумага (100 руб)")
    print("  3 - Корзина (200 руб)")

    return safe_input_int("Ваш выбор (1-3): ", min_value=1, max_value=3)


def get_delivery():
    """
    Запрашивает необходимость доставки.

    Returns:
        bool: True если доставка нужна, False если нет
    """
    print("\n--- ДОСТАВКА ---")
    return safe_input_bool("Нужна доставка?", default=False)


def get_card():
    """
    Запрашивает необходимость открытки.

    Returns:
        bool: True если открытка нужна, False если нет
    """
    print("\n--- ОТКРЫТКА ---")
    return safe_input_bool("Нужна открытка?", default=False)


def get_self_pickup():
    """
    Запрашивает самовывоз.

    Returns:
        bool: True если самовывоз, False если нет
    """
    print("\n--- САМОВЫВОЗ ---")
    return safe_input_bool("Самовывоз?", default=False)


def get_user_data():
    """
    Запрашивает у пользователя данные для расчета стоимости букета.

    Returns:
        dict: Словарь с данными пользователя:
            - flower_type (int): тип цветов (1-3)
            - quantity (int): количество цветов
            - packaging (int): тип упаковки (1-3)
            - delivery (bool): нужна ли доставка
            - card (bool): нужна ли открытка
            - self_pickup (bool): самовывоз
    """
    print("\n" + "="*60)
    print(" " * 15 + "КАЛЬКУЛЯТОР СТОИМОСТИ БУКЕТА")
    print("="*60)

    # Сбор всех данных
    flower_type = get_flower_type()
    quantity = get_quantity()
    packaging = get_packaging_type()
    delivery = get_delivery()
    card = get_card()
    self_pickup = get_self_pickup()

    # Формируем словарь с данными
    user_data = {
        'flower_type': flower_type,
        'quantity': quantity,
        'packaging': packaging,
        'delivery': delivery,
        'card': card,
        'self_pickup': self_pickup
    }

    return user_data


def show_result(result_data):
    """
    Выводит результат расчета стоимости букета.

    Args:
        result_data (dict): Словарь с результатами расчета:
            - base_cost (float): базовая стоимость цветов
            - packaging_cost (float): стоимость упаковки
            - services_cost (float): стоимость доп. услуг
            - discount (float): сумма скидки
            - total_cost (float): итоговая стоимость
    """
    print("\n" + "="*60)
    print(" " * 20 + "РЕЗУЛЬТАТ РАСЧЕТА")
    print("="*60)

    # Вывод детализации
    print(f"\n{'Базовая стоимость цветов:':<30} {result_data['base_cost']:>10.2f} руб")
    print(f"{'Стоимость упаковки:':<30} {result_data['packaging_cost']:>10.2f} руб")
    print(f"{'Дополнительные услуги:':<30} {result_data['services_cost']:>10.2f} руб")
    print(f"{'Скидка:':<30} -{result_data['discount']:>10.2f} руб")

    # Разделитель
    print("-"*60)

    # Итоговая сумма
    print(f"{'ИТОГО К ОПЛАТЕ:':<30} {result_data['total_cost']:>10.2f} руб")
    print("="*60 + "\n")


def show_user_data(user_data):
    """
    Выводит введенные пользователем данные для проверки.

    Args:
        user_data (dict): Словарь с данными пользователя
    """
    print("\n" + "="*60)
    print(" " * 18 + "ВВЕДЕННЫЕ ДАННЫЕ")
    print("="*60)

    # Словарь для преобразования кодов в названия
    flower_names = {1: "Розы", 2: "Тюльпаны", 3: "Хризантемы"}
    packaging_names = {1: "Лента", 2: "Бумага", 3: "Корзина"}

    print(f"\n{'Тип цветов:':<20} {flower_names[user_data['flower_type']]}")
    print(f"{'Количество:':<20} {user_data['quantity']} шт")
    print(f"{'Упаковка:':<20} {packaging_names[user_data['packaging']]}")
    print(f"{'Доставка:':<20} {'Да' if user_data['delivery'] else 'Нет'}")
    print(f"{'Открытка:':<20} {'Да' if user_data['card'] else 'Нет'}")
    print(f"{'Самовывоз:':<20} {'Да' if user_data['self_pickup'] else 'Нет'}")
    print("="*60 + "\n")


def show_error(message):
    """
    Выводит сообщение об ошибке.

    Args:
        message (str): Текст сообщения об ошибке
    """
    print(f"\n❌ ОШИБКА: {message}\n")


def show_info(message):
    """
    Выводит информационное сообщение.

    Args:
        message (str): Текст информационного сообщения
    """
    print(f"\nℹ️ {message}\n")


def show_success(message):
    """
    Выводит сообщение об успешном выполнении.

    Args:
        message (str): Текст сообщения об успехе
    """
    print(f"\n✅ {message}\n")