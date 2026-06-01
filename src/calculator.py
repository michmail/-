"""
Модуль основной логики расчета стоимости букета.
"""

from typing import Dict

FLOWER_PRICES = {
    1: {"name": "Розы", "price": 150},
    2: {"name": "Тюльпаны", "price": 80},
    3: {"name": "Хризантемы", "price": 100}
}

PACKAGING_PRICES = {
    1: {"name": "Лента", "price": 50},
    2: {"name": "Бумага", "price": 100},
    3: {"name": "Корзина", "price": 200}
}

SERVICE_PRICES = {
    "delivery": 300,
    "card": 50
}


def calculate_base_cost(flower_type: int, quantity: int) -> float:
    if flower_type not in FLOWER_PRICES:
        raise ValueError(f"Неизвестный тип цветов: {flower_type}")
    if quantity <= 0:
        raise ValueError("Количество цветов должно быть положительным")
    return FLOWER_PRICES[flower_type]["price"] * quantity


def calculate_packaging_cost(packaging_type: int) -> float:
    if packaging_type not in PACKAGING_PRICES:
        raise ValueError(f"Неизвестный тип упаковки: {packaging_type}")
    return PACKAGING_PRICES[packaging_type]["price"]


def calculate_services_cost(delivery: bool, card: bool) -> float:
    total = 0.0
    if delivery:
        total += SERVICE_PRICES["delivery"]
    if card:
        total += SERVICE_PRICES["card"]
    return total


def calculate_total(flower_type: int, quantity: int, packaging_type: int,
                    delivery: bool, card: bool) -> Dict:
    base = calculate_base_cost(flower_type, quantity)
    packaging = calculate_packaging_cost(packaging_type)
    services = calculate_services_cost(delivery, card)

    return {
        "base_cost": base,
        "packaging_cost": packaging,
        "services_cost": services,
        "total_cost": base + packaging + services,
        "flower_name": FLOWER_PRICES[flower_type]["name"],
        "packaging_name": PACKAGING_PRICES[packaging_type]["name"]
    }