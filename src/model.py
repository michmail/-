"""
Модуль математической модели для оптимизации выбора букета.

Содержит функции для:
- поиска оптимального букета под заданный бюджет
- сравнения нескольких вариантов букетов
- подбора максимального количества цветов

Author: [Твое имя]
Date: 2026-03-26
"""

from typing import List, Dict, Tuple, Optional
import itertools

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

# Цены на услуги (руб)
SERVICE_PRICES = {
    "delivery": 300,
    "card": 50
}


def calculate_bouquet_price(
        flower_type: int,
        quantity: int,
        packaging_type: int,
        delivery: bool,
        card: bool,
        self_pickup: bool
) -> float:
    """
    Рассчитывает стоимость букета по заданным параметрам.

    Returns:
        float: Итоговая стоимость
    """
    # Базовая стоимость цветов
    flower_cost = FLOWER_PRICES[flower_type]["price"] * quantity

    # Упаковка
    packaging_cost = PACKAGING_PRICES[packaging_type]["price"]

    # Услуги
    services_cost = 0
    if delivery:
        services_cost += SERVICE_PRICES["delivery"]
    if card:
        services_cost += SERVICE_PRICES["card"]

    # Промежуточная сумма
    subtotal = flower_cost + packaging_cost + services_cost

    # Скидка
    discount_rate = 0
    if quantity > 20:
        discount_rate += 0.05
    if self_pickup:
        discount_rate += 0.05
    discount_rate = min(discount_rate, 0.10)

    discount = subtotal * discount_rate

    return subtotal - discount


def find_optimal_for_budget(
        budget: float,
        flower_type: Optional[int] = None,
        need_delivery: bool = False,
        need_card: bool = False
) -> Dict:
    """
    Находит оптимальный вариант букета под заданный бюджет.

    Args:
        budget (float): Максимальная сумма
        flower_type (int, optional): Желаемый тип цветов (1-3)
        need_delivery (bool): Нужна ли доставка
        need_card (bool): Нужна ли открытка

    Returns:
        dict: Оптимальный вариант букета:
            - flower_type (int): тип цветов
            - quantity (int): количество цветов
            - packaging_type (int): тип упаковки
            - delivery (bool): доставка
            - card (bool): открытка
            - self_pickup (bool): самовывоз
            - total_cost (float): итоговая стоимость
            - remaining (float): остаток от бюджета

    Examples:
        >>> result = find_optimal_for_budget(1000)
        >>> result['total_cost'] <= 1000
        True
    """
    best_result = None
    best_quantity = 0

    # Определяем какие цветы проверять
    flower_types = [flower_type] if flower_type else [1, 2, 3]

    # Типы упаковки (все)
    packaging_types = [1, 2, 3]

    # Самовывоз (если доставка не нужна, можно самовывоз)
    self_pickup_options = [True, False] if not need_delivery else [False]

    # Перебираем все комбинации
    for f_type in flower_types:
        for p_type in packaging_types:
            for self_pickup in self_pickup_options:
                # Подбираем максимальное количество цветов
                price_per_flower = FLOWER_PRICES[f_type]["price"]
                packaging_cost = PACKAGING_PRICES[p_type]["price"]

                services_cost = 0
                if need_delivery:
                    services_cost += SERVICE_PRICES["delivery"]
                if need_card:
                    services_cost += SERVICE_PRICES["card"]

                # Учитываем скидку за самовывоз
                base_subtotal_without_flowers = packaging_cost + services_cost
                if self_pickup:
                    # Скидка 5% применяется к полной сумме
                    # Поэтому нужно решать уравнение
                    pass

                # Простой перебор количества цветов
                for quantity in range(1, 101):  # от 1 до 100 цветов
                    total = calculate_bouquet_price(
                        f_type, quantity, p_type,
                        need_delivery, need_card, self_pickup
                    )

                    if total <= budget and quantity > best_quantity:
                        best_quantity = quantity
                        best_result = {
                            'flower_type': f_type,
                            'flower_name': FLOWER_PRICES[f_type]["name"],
                            'quantity': quantity,
                            'packaging_type': p_type,
                            'packaging_name': PACKAGING_PRICES[p_type]["name"],
                            'delivery': need_delivery,
                            'card': need_card,
                            'self_pickup': self_pickup,
                            'total_cost': total,
                            'remaining': budget - total
                        }

    if best_result is None:
        # Если ничего не найдено, возвращаем минимальный вариант
        return {
            'flower_type': 1,
            'flower_name': "Розы",
            'quantity': 1,
            'packaging_type': 1,
            'packaging_name': "Лента",
            'delivery': need_delivery,
            'card': need_card,
            'self_pickup': True,
            'total_cost': 100,  # примерная минимальная цена
            'remaining': budget - 100,
            'error': 'Бюджет слишком мал'
        }

    return best_result


def compare_options(option1: Dict, option2: Dict) -> Dict:
    """
    Сравнивает два варианта букета.

    Args:
        option1 (dict): Первый вариант
        option2 (dict): Второй вариант

    Returns:
        dict: Результат сравнения
    """
    diff = option1['total_cost'] - option2['total_cost']

    cheaper = option1 if diff < 0 else option2
    more_expensive = option2 if diff < 0 else option1

    return {
        'cheaper': cheaper,
        'more_expensive': more_expensive,
        'difference': abs(diff),
        'cheaper_by_percent': (abs(diff) / more_expensive['total_cost']) * 100
    }


def get_best_value_for_budget(budget: float) -> Dict:
    """
    Находит вариант с максимальным количеством цветов за бюджет.

    Args:
        budget (float): Бюджет

    Returns:
        dict: Лучший вариант по соотношению цена/количество
    """
    best_result = None
    best_flowers_per_ruble = 0

    for f_type in [1, 2, 3]:
        for p_type in [1, 2, 3]:
            for quantity in range(1, 101):
                # Вариант с самовывозом (дешевле)
                total_self = calculate_bouquet_price(
                    f_type, quantity, p_type,
                    False, False, True
                )

                if total_self <= budget:
                    flowers_per_ruble = quantity / total_self
                    if flowers_per_ruble > best_flowers_per_ruble:
                        best_flowers_per_ruble = flowers_per_ruble
                        best_result = {
                            'flower_type': f_type,
                            'flower_name': FLOWER_PRICES[f_type]["name"],
                            'quantity': quantity,
                            'packaging_type': p_type,
                            'packaging_name': PACKAGING_PRICES[p_type]["name"],
                            'delivery': False,
                            'card': False,
                            'self_pickup': True,
                            'total_cost': total_self,
                            'remaining': budget - total_self,
                            'flowers_per_ruble': flowers_per_ruble
                        }

    return best_result


def suggest_bouquet_by_preferences(
        budget: float,
        prefer_roses: bool = False,
        prefer_luxury_packaging: bool = False,
        need_delivery: bool = False
) -> Dict:
    """
    Предлагает букет на основе предпочтений пользователя.

    Args:
        budget (float): Бюджет
        prefer_roses (bool): Предпочитает розы
        prefer_luxury_packaging (bool): Предпочитает дорогую упаковку
        need_delivery (bool): Нужна доставка

    Returns:
        dict: Рекомендованный вариант
    """
    # Определяем тип цветов
    if prefer_roses:
        flower_type = 1  # Розы
    else:
        flower_type = 2  # Тюльпаны (оптимальнее)

    # Определяем тип упаковки
    if prefer_luxury_packaging:
        packaging_type = 3  # Корзина
    else:
        packaging_type = 1  # Лента (дешевле)

    # Подбираем количество
    for quantity in range(100, 0, -1):  # от максимума к минимуму
        total = calculate_bouquet_price(
            flower_type, quantity, packaging_type,
            need_delivery, False, not need_delivery
        )

        if total <= budget:
            return {
                'flower_type': flower_type,
                'flower_name': FLOWER_PRICES[flower_type]["name"],
                'quantity': quantity,
                'packaging_type': packaging_type,
                'packaging_name': PACKAGING_PRICES[packaging_type]["name"],
                'delivery': need_delivery,
                'card': False,
                'self_pickup': not need_delivery,
                'total_cost': total,
                'remaining': budget - total,
                'recommended': True
            }

    # Если ничего не подошло
    return find_optimal_for_budget(budget, flower_type, need_delivery)


# Экспорт
__all__ = [
    'calculate_bouquet_price',
    'find_optimal_for_budget',
    'compare_options',
    'get_best_value_for_budget',
    'suggest_bouquet_by_preferences'
]