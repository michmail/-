"""
Модуль основной логики расчета стоимости букета.

Содержит функции для расчета:
- базовой стоимости цветов
- стоимости упаковки
- стоимости дополнительных услуг
- полной стоимости букета

Author: [Твое имя]
Date: 2026-03-26
"""

# Цены на цветы (руб/шт)
FLOWER_PRICES = {
    1: {"name": "Розы", "price": 150},
    2: {"name": "Тюльпаны", "price": 80},
    3: {"name": "Хризантемы", "price": 100}
}

# Цены на упаковку (руб)
PACKAGING_PRICES = {
    1: {"name": "Лента", "price": 50},
    2: {"name": "Бумага", "price": 100},
    3: {"name": "Корзина", "price": 200}
}

# Цены на дополнительные услуги (руб)
SERVICE_PRICES = {
    "delivery": 300,  # Доставка
    "card": 50  # Открытка
}


def calculate_base_cost(flower_type, quantity):
    """
    Рассчитывает базовую стоимость цветов.

    Формула: цена_цветка × количество

    Args:
        flower_type (int): Тип цветов (1 - розы, 2 - тюльпаны, 3 - хризантемы)
        quantity (int): Количество цветов (положительное целое число)

    Returns:
        float: Базовая стоимость цветов

    Raises:
        ValueError: Если тип цветов не существует или количество <= 0

    Examples:
        >>> calculate_base_cost(1, 10)  # 10 роз
        1500.0
        >>> calculate_base_cost(2, 5)   # 5 тюльпанов
        400.0
    """
    # Проверка типа цветов
    if flower_type not in FLOWER_PRICES:
        raise ValueError(
            f"Неизвестный тип цветов: {flower_type}. "
            f"Допустимые значения: {list(FLOWER_PRICES.keys())}"
        )

    # Проверка количества
    if quantity <= 0:
        raise ValueError(f"Количество цветов должно быть положительным. Получено: {quantity}")

    if quantity > 1000:
        raise ValueError(f"Количество цветов не может превышать 1000. Получено: {quantity}")

    # Расчет
    price_per_flower = FLOWER_PRICES[flower_type]["price"]
    base_cost = price_per_flower * quantity

    return float(base_cost)


def calculate_packaging_cost(packaging_type):
    """
    Рассчитывает стоимость упаковки.

    Args:
        packaging_type (int): Тип упаковки (1 - лента, 2 - бумага, 3 - корзина)

    Returns:
        float: Стоимость упаковки

    Raises:
        ValueError: Если тип упаковки не существует

    Examples:
        >>> calculate_packaging_cost(1)  # Лента
        50.0
        >>> calculate_packaging_cost(3)  # Корзина
        200.0
    """
    if packaging_type not in PACKAGING_PRICES:
        raise ValueError(
            f"Неизвестный тип упаковки: {packaging_type}. "
            f"Допустимые значения: {list(PACKAGING_PRICES.keys())}"
        )

    return float(PACKAGING_PRICES[packaging_type]["price"])


def calculate_services_cost(delivery, card):
    """
    Рассчитывает стоимость дополнительных услуг.

    Args:
        delivery (bool): Нужна ли доставка (True/False)
        card (bool): Нужна ли открытка (True/False)

    Returns:
        float: Стоимость дополнительных услуг

    Examples:
        >>> calculate_services_cost(True, False)  # Только доставка
        300.0
        >>> calculate_services_cost(True, True)   # Доставка и открытка
        350.0
        >>> calculate_services_cost(False, False) # Без услуг
        0.0
    """
    total = 0.0

    if delivery:
        total += SERVICE_PRICES["delivery"]

    if card:
        total += SERVICE_PRICES["card"]

    return total


def calculate_subtotal(flower_type, quantity, packaging_type, delivery, card):
    """
    Рассчитывает промежуточную сумму (без скидки).

    Args:
        flower_type (int): Тип цветов
        quantity (int): Количество цветов
        packaging_type (int): Тип упаковки
        delivery (bool): Нужна ли доставка
        card (bool): Нужна ли открытка

    Returns:
        float: Промежуточная сумма до применения скидки

    Raises:
        ValueError: При некорректных входных данных
    """
    base_cost = calculate_base_cost(flower_type, quantity)
    packaging_cost = calculate_packaging_cost(packaging_type)
    services_cost = calculate_services_cost(delivery, card)

    subtotal = base_cost + packaging_cost + services_cost

    return subtotal


def get_flower_name(flower_type):
    """
    Возвращает название цветов по коду.

    Args:
        flower_type (int): Тип цветов (1-3)

    Returns:
        str: Название цветов

    Raises:
        ValueError: Если тип цветов не существует
    """
    if flower_type not in FLOWER_PRICES:
        raise ValueError(f"Неизвестный тип цветов: {flower_type}")

    return FLOWER_PRICES[flower_type]["name"]


def get_packaging_name(packaging_type):
    """
    Возвращает название упаковки по коду.

    Args:
        packaging_type (int): Тип упаковки (1-3)

    Returns:
        str: Название упаковки

    Raises:
        ValueError: Если тип упаковки не существует
    """
    if packaging_type not in PACKAGING_PRICES:
        raise ValueError(f"Неизвестный тип упаковки: {packaging_type}")

    return PACKAGING_PRICES[packaging_type]["name"]


def get_flower_price(flower_type):
    """
    Возвращает цену одного цветка.

    Args:
        flower_type (int): Тип цветов (1-3)

    Returns:
        float: Цена одного цветка

    Raises:
        ValueError: Если тип цветов не существует
    """
    if flower_type not in FLOWER_PRICES:
        raise ValueError(f"Неизвестный тип цветов: {flower_type}")

    return float(FLOWER_PRICES[flower_type]["price"])


def get_packaging_price(packaging_type):
    """
    Возвращает цену упаковки.

    Args:
        packaging_type (int): Тип упаковки (1-3)

    Returns:
        float: Цена упаковки

    Raises:
        ValueError: Если тип упаковки не существует
    """
    if packaging_type not in PACKAGING_PRICES:
        raise ValueError(f"Неизвестный тип упаковки: {packaging_type}")

    return float(PACKAGING_PRICES[packaging_type]["price"])


def get_service_price(service_name):
    """
    Возвращает цену услуги по названию.

    Args:
        service_name (str): Название услуги ('delivery' или 'card')

    Returns:
        float: Цена услуги

    Raises:
        ValueError: Если услуга не существует
    """
    if service_name not in SERVICE_PRICES:
        raise ValueError(f"Неизвестная услуга: {service_name}")

    return float(SERVICE_PRICES[service_name])


def calculate_full_price(user_data):
    """
    Рассчитывает полную стоимость букета на основе данных пользователя.

    Это основная функция, которая объединяет все расчеты.

    Args:
        user_data (dict): Словарь с данными пользователя, содержащий:
            - flower_type (int): Тип цветов
            - quantity (int): Количество цветов
            - packaging (int): Тип упаковки
            - delivery (bool): Нужна ли доставка
            - card (bool): Нужна ли открытка

    Returns:
        dict: Словарь с детализацией расчета:
            - base_cost (float): базовая стоимость цветов
            - packaging_cost (float): стоимость упаковки
            - services_cost (float): стоимость услуг
            - subtotal (float): промежуточная сумма

    Examples:
        >>> user_data = {'flower_type': 1, 'quantity': 10, 'packaging': 2,
        ...              'delivery': True, 'card': False}
        >>> result = calculate_full_price(user_data)
        >>> result['base_cost']
        1500.0
    """
    # Проверка наличия всех необходимых ключей
    required_keys = ['flower_type', 'quantity', 'packaging', 'delivery', 'card']
    for key in required_keys:
        if key not in user_data:
            raise KeyError(f"Отсутствует обязательный ключ в user_data: {key}")

    # Расчет
    base_cost = calculate_base_cost(user_data['flower_type'], user_data['quantity'])
    packaging_cost = calculate_packaging_cost(user_data['packaging'])
    services_cost = calculate_services_cost(user_data['delivery'], user_data['card'])
    subtotal = base_cost + packaging_cost + services_cost

    return {
        'base_cost': base_cost,
        'packaging_cost': packaging_cost,
        'services_cost': services_cost,
        'subtotal': subtotal
    }


def calculate_total(user_data: Dict) -> Dict:
    """
    Главная функция расчета полной стоимости букета.
    Объединяет все модули: calculator, discounts.

    Args:
        user_data (dict): Словарь с данными пользователя:
            - flower_type (int): тип цветов (1-3)
            - quantity (int): количество цветов
            - packaging (int): тип упаковки (1-3)
            - delivery (bool): доставка
            - card (bool): открытка
            - self_pickup (bool): самовывоз

    Returns:
        dict: Полный результат расчета:
            - base_cost (float): стоимость цветов
            - packaging_cost (float): стоимость упаковки
            - services_cost (float): стоимость услуг
            - subtotal (float): промежуточная сумма
            - discount (float): сумма скидки
            - discount_rate (float): процент скидки
            - total_cost (float): итоговая сумма

    Examples:
        >>> user_data = {'flower_type': 1, 'quantity': 15, 'packaging': 2,
        ...              'delivery': True, 'card': False, 'self_pickup': False}
        >>> result = calculate_total(user_data)
        >>> result['total_cost']
        2650.0
    """
    from discounts import calculate_discount

    # 1. Базовая стоимость цветов
    base_cost = calculate_base_cost(
        user_data['flower_type'],
        user_data['quantity']
    )

    # 2. Стоимость упаковки
    packaging_cost = calculate_packaging_cost(
        user_data['packaging']
    )

    # 3. Стоимость услуг
    services_cost = calculate_services_cost(
        user_data['delivery'],
        user_data['card']
    )

    # 4. Промежуточная сумма
    subtotal = base_cost + packaging_cost + services_cost

    # 5. Скидка
    discount = calculate_discount(
        user_data['quantity'],
        user_data['self_pickup'],
        subtotal,
        flower_type=user_data['flower_type']
    )

    # 6. Процент скидки
    discount_rate = 0
    if subtotal > 0:
        discount_rate = (discount / subtotal) * 100

    # 7. Итоговая стоимость
    total_cost = subtotal - discount

    return {
        'base_cost': base_cost,
        'packaging_cost': packaging_cost,
        'services_cost': services_cost,
        'subtotal': subtotal,
        'discount': discount,
        'discount_rate': discount_rate,
        'total_cost': total_cost
    }

# Словари для внешнего использования
__all__ = [
    'FLOWER_PRICES',
    'PACKAGING_PRICES',
    'SERVICE_PRICES',
    'calculate_base_cost',
    'calculate_packaging_cost',
    'calculate_services_cost',
    'calculate_subtotal',
    'calculate_total',           # ← новая функция
    'get_flower_name',
    'get_packaging_name',
    'get_flower_price',
    'get_packaging_price',
    'get_service_price',
    'calculate_full_price'
]