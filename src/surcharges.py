"""
Модуль скидок и надбавок.
"""


def apply_discount(total_cost: float, quantity: int) -> float:
    if quantity >= 100:
        discount = 0.15
    elif quantity >= 50:
        discount = 0.10
    else:
        discount = 0.0
    return total_cost * (1 - discount)


def get_discount_info(quantity: int) -> str:
    if quantity >= 100:
        return "Скидка 15% за количество >100 цветов"
    elif quantity >= 50:
        return "Скидка 10% за количество >50 цветов"
    else:
        return "Скидка не применена"