"""
Модуль расчета скидок и дополнительных правил.

Содержит функции для:
- расчета скидки на букет
- расчета процента скидки
- применения сезонных скидок
- расчета скидки за повторный заказ

Правила скидок:
1. 5% скидка при количестве цветов > 20
2. 5% скидка при самовывозе
3. Скидки суммируются, но максимум 10%
4. Сезонная скидка 10% на тюльпаны в марте
5. Скидка 3% для постоянных клиентов (от 5 заказов)

Author: [Твое имя]
Date: 2026-03-26
"""

import datetime


def calculate_discount(quantity, self_pickup, subtotal, flower_type=None, repeat_customer=False):
    """
    Рассчитывает сумму скидки на основе различных условий.

    Формула скидки:
    discount_amount = subtotal × discount_rate

    discount_rate рассчитывается как сумма всех применимых скидок,
    но не более 0.10 (10%).

    Args:
        quantity (int): Количество цветов
        self_pickup (bool): Самовывоз (True - самовывоз, False - доставка)
        subtotal (float): Промежуточная сумма до скидки
        flower_type (int, optional): Тип цветов (1-3) для сезонной скидки
        repeat_customer (bool, optional): Постоянный клиент (True/False)

    Returns:
        float: Сумма скидки

    Examples:
        >>> calculate_discount(25, True, 1000)  # 25 цветов + самовывоз
        100.0  # 10% от 1000
        >>> calculate_discount(25, False, 1000)  # только 25 цветов
        50.0   # 5% от 1000
        >>> calculate_discount(10, True, 1000)   # только самовывоз
        50.0   # 5% от 1000
        >>> calculate_discount(10, False, 1000)  # без скидок
        0.0
    """
    discount_rate = 0.0

    # 1. Скидка за количество цветов (>20 штук)
    if quantity > 20:
        discount_rate += 0.05
        print(f"  ✓ Скидка за количество (>20): +5%")

    # 2. Скидка за самовывоз
    if self_pickup:
        discount_rate += 0.05
        print(f"  ✓ Скидка за самовывоз: +5%")

    # 3. Сезонная скидка (тюльпаны в марте - 10%)
    seasonal_discount = _calculate_seasonal_discount(flower_type)
    if seasonal_discount > 0:
        discount_rate += seasonal_discount
        print(f"  ✓ Сезонная скидка: +{seasonal_discount * 100}%")

    # 4. Скидка для постоянных клиентов
    if repeat_customer:
        discount_rate += 0.03
        print(f"  ✓ Скидка постоянному клиенту: +3%")

    # Ограничиваем максимальную скидку 10%
    original_rate = discount_rate
    discount_rate = min(discount_rate, 0.10)

    if original_rate > 0.10:
        print(f"  ⚠ Скидка ограничена 10% (было {original_rate * 100}%)")

    # Рассчитываем сумму скидки
    discount_amount = subtotal * discount_rate

    # Выводим информацию о скидке
    if discount_rate > 0:
        print(f"\n  Итоговая скидка: {discount_rate * 100}%")
        print(f"  Сумма скидки: {discount_amount:.2f} руб")
    else:
        print(f"  Скидка не применяется")

    return discount_amount


def _calculate_seasonal_discount(flower_type):
    """
    Рассчитывает сезонную скидку.

    Сезонные акции:
    - Март: тюльпаны (тип 2) - скидка 10%
    - Сентябрь: хризантемы (тип 3) - скидка 10%
    - Июнь-август: розы (тип 1) - скидка 5%

    Args:
        flower_type (int, optional): Тип цветов (1-3)

    Returns:
        float: Процент скидки (0.0 - 0.10)
    """
    if flower_type is None:
        return 0.0

    now = datetime.datetime.now()
    current_month = now.month

    # Тюльпаны в марте (месяц 3) - скидка 10%
    if flower_type == 2 and current_month == 3:
        return 0.10

    # Хризантемы в сентябре (месяц 9) - скидка 10%
    if flower_type == 3 and current_month == 9:
        return 0.10

    # Розы летом (июнь, июль, август) - скидка 5%
    if flower_type == 1 and current_month in [6, 7, 8]:
        return 0.05

    return 0.0


def get_discount_rate(quantity, self_pickup, flower_type=None, repeat_customer=False):
    """
    Возвращает процент скидки без расчета суммы.

    Args:
        quantity (int): Количество цветов
        self_pickup (bool): Самовывоз
        flower_type (int, optional): Тип цветов для сезонной скидки
        repeat_customer (bool, optional): Постоянный клиент

    Returns:
        float: Процент скидки (0.0 - 0.10)

    Examples:
        >>> get_discount_rate(25, True)
        0.10
        >>> get_discount_rate(25, False)
        0.05
        >>> get_discount_rate(10, True)
        0.05
    """
    discount_rate = 0.0

    if quantity > 20:
        discount_rate += 0.05

    if self_pickup:
        discount_rate += 0.05

    seasonal = _calculate_seasonal_discount(flower_type)
    discount_rate += seasonal

    if repeat_customer:
        discount_rate += 0.03

    return min(discount_rate, 0.10)


def calculate_bulk_discount(quantity, price_per_item):
    """
    Рассчитывает оптовую скидку при покупке большого количества.

    Правила:
    - 50+ цветов: скидка 5%
    - 100+ цветов: скидка 10%
    - 200+ цветов: скидка 15%

    Args:
        quantity (int): Количество цветов
        price_per_item (float): Цена за один цветок

    Returns:
        float: Сумма оптовой скидки

    Examples:
        >>> calculate_bulk_discount(50, 150)  # 50 роз по 150 руб
        375.0  # 5% от 7500
    """
    subtotal = quantity * price_per_item

    if quantity >= 200:
        discount_rate = 0.15
    elif quantity >= 100:
        discount_rate = 0.10
    elif quantity >= 50:
        discount_rate = 0.05
    else:
        discount_rate = 0.0

    return subtotal * discount_rate


def calculate_loyalty_discount(order_count):
    """
    Рассчитывает скидку для постоянных клиентов.

    Правила:
    - 5-9 заказов: скидка 3%
    - 10-24 заказа: скидка 5%
    - 25+ заказов: скидка 10%

    Args:
        order_count (int): Количество предыдущих заказов

    Returns:
        float: Процент скидки (0.0 - 0.10)

    Examples:
        >>> calculate_loyalty_discount(5)
        0.03
        >>> calculate_loyalty_discount(10)
        0.05
    """
    if order_count >= 25:
        return 0.10
    elif order_count >= 10:
        return 0.05
    elif order_count >= 5:
        return 0.03
    else:
        return 0.0


def calculate_promo_discount(promo_code, subtotal):
    """
    Рассчитывает скидку по промокоду.

    Доступные промокоды:
    - "FLOWER10": скидка 10%
    - "WELCOME5": скидка 5%
    - "LOVE15": скидка 15% (максимум 500 руб)

    Args:
        promo_code (str): Промокод
        subtotal (float): Сумма до скидки

    Returns:
        float: Сумма скидки

    Examples:
        >>> calculate_promo_discount("FLOWER10", 1000)
        100.0
        >>> calculate_promo_discount("LOVE15", 1000)
        150.0
    """
    if not promo_code:
        return 0.0

    promo_code = promo_code.upper().strip()

    if promo_code == "FLOWER10":
        return subtotal * 0.10
    elif promo_code == "WELCOME5":
        return subtotal * 0.05
    elif promo_code == "LOVE15":
        # Максимум 500 руб
        discount = subtotal * 0.15
        return min(discount, 500.0)
    else:
        return 0.0


def calculate_total_discount(
        quantity,
        self_pickup,
        subtotal,
        flower_type=None,
        repeat_customer=False,
        promo_code=None,
        order_count=0
):
    """
    Рассчитывает ОБЩУЮ сумму всех скидок.

    Эта функция объединяет все виды скидок:
    - Стандартные скидки (количество, самовывоз)
    - Сезонные скидки
    - Скидки постоянным клиентам
    - Промокоды

    Args:
        quantity (int): Количество цветов
        self_pickup (bool): Самовывоз
        subtotal (float): Промежуточная сумма
        flower_type (int, optional): Тип цветов
        repeat_customer (bool, optional): Постоянный клиент
        promo_code (str, optional): Промокод
        order_count (int, optional): Количество предыдущих заказов

    Returns:
        dict: Словарь с детализацией всех скидок:
            - standard_discount (float): Стандартная скидка
            - seasonal_discount (float): Сезонная скидка
            - loyalty_discount (float): Скидка постоянному клиенту
            - promo_discount (float): Скидка по промокоду
            - total_discount (float): Общая сумма скидки
            - total_discount_rate (float): Общий процент скидки

    Examples:
        >>> result = calculate_total_discount(25, True, 1000)
        >>> result['total_discount']
        100.0
    """
    result = {
        'standard_discount': 0.0,
        'seasonal_discount': 0.0,
        'loyalty_discount': 0.0,
        'promo_discount': 0.0,
        'total_discount': 0.0,
        'total_discount_rate': 0.0
    }

    # 1. Стандартная скидка
    standard_rate = 0.0
    if quantity > 20:
        standard_rate += 0.05
    if self_pickup:
        standard_rate += 0.05
    standard_rate = min(standard_rate, 0.10)
    result['standard_discount'] = subtotal * standard_rate

    # 2. Сезонная скидка
    seasonal_rate = _calculate_seasonal_discount(flower_type)
    result['seasonal_discount'] = subtotal * seasonal_rate

    # 3. Скидка постоянному клиенту
    loyalty_rate = calculate_loyalty_discount(order_count)
    result['loyalty_discount'] = subtotal * loyalty_rate

    # 4. Скидка по промокоду
    result['promo_discount'] = calculate_promo_discount(promo_code, subtotal)

    # Суммируем все скидки (но не более 30% от суммы)
    result['total_discount'] = sum([
        result['standard_discount'],
        result['seasonal_discount'],
        result['loyalty_discount'],
        result['promo_discount']
    ])

    # Ограничиваем максимальную скидку 30%
    max_discount = subtotal * 0.30
    if result['total_discount'] > max_discount:
        result['total_discount'] = max_discount

    # Рассчитываем общий процент скидки
    if subtotal > 0:
        result['total_discount_rate'] = result['total_discount'] / subtotal

    return result


def can_apply_discount(quantity, self_pickup):
    """
    Проверяет, можно ли применить скидку.

    Args:
        quantity (int): Количество цветов
        self_pickup (bool): Самовывоз

    Returns:
        bool: True если есть хоть какая-то скидка

    Examples:
        >>> can_apply_discount(25, True)
        True
        >>> can_apply_discount(10, False)
        False
    """
    return quantity > 20 or self_pickup


def get_discount_description(discount_rate):
    """
    Возвращает текстовое описание скидки.

    Args:
        discount_rate (float): Процент скидки (0.0 - 0.10)

    Returns:
        str: Текстовое описание скидки
    """
    if discount_rate >= 0.10:
        return "Максимальная скидка!"
    elif discount_rate >= 0.05:
        return "Хорошая скидка"
    elif discount_rate > 0:
        return "Небольшая скидка"
    else:
        return "Скидка не применяется"


# Словарь для экспорта
__all__ = [
    'calculate_discount',
    'get_discount_rate',
    'calculate_bulk_discount',
    'calculate_loyalty_discount',
    'calculate_promo_discount',
    'calculate_total_discount',
    'can_apply_discount',
    'get_discount_description'
]