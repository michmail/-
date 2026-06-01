"""
Главный модуль программы.
"""

from input_output import (
    get_flower_type, get_quantity, get_packaging_type,
    get_delivery, get_card, print_result
)
from calculator import calculate_total
from surcharges import apply_discount, get_discount_info
from logger import log_result


def main():
    print("\n" + "=" * 40)
    print("ДОБРО ПОЖАЛОВАТЬ В КАЛЬКУЛЯТОР БУКЕТА")
    print("=" * 40)

    flower_type = get_flower_type()
    quantity = get_quantity()
    packaging_type = get_packaging_type()
    delivery = get_delivery()
    card = get_card()

    result = calculate_total(flower_type, quantity, packaging_type, delivery, card)
    result["quantity"] = quantity
    result["delivery"] = delivery
    result["card"] = card

    original_total = result["total_cost"]
    discounted_total = apply_discount(original_total, quantity)

    if discounted_total < original_total:
        result["total_cost"] = discounted_total
        print(f"\n💡 {get_discount_info(quantity)}")
        print(f"💰 Экономия: {original_total - discounted_total:.2f} руб")

    print_result(result)
    log_result(result)
    print("\nСпасибо за использование калькулятора!")


if __name__ == "__main__":
    main()