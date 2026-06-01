"""
Модуль сравнения двух вариантов букетов.
"""

from calculator import calculate_total
from input_output import (
    get_flower_type, get_quantity, get_packaging_type, get_delivery, get_card
)


def compare_two_bouquets():
    print("\n" + "=" * 40)
    print("СРАВНЕНИЕ ДВУХ ВАРИАНТОВ БУКЕТА")
    print("=" * 40)

    print("\n--- ВАРИАНТ 1 ---")
    f1 = get_flower_type()
    q1 = get_quantity()
    p1 = get_packaging_type()
    d1 = get_delivery()
    c1 = get_card()

    print("\n--- ВАРИАНТ 2 ---")
    f2 = get_flower_type()
    q2 = get_quantity()
    p2 = get_packaging_type()
    d2 = get_delivery()
    c2 = get_card()

    r1 = calculate_total(f1, q1, p1, d1, c1)
    r2 = calculate_total(f2, q2, p2, d2, c2)

    print("\n" + "=" * 40)
    print(f"Вариант 1: {r1['total_cost']} руб")
    print(f"Вариант 2: {r2['total_cost']} руб")

    if r1['total_cost'] < r2['total_cost']:
        print("👉 Вариант 1 дешевле")
    elif r2['total_cost'] < r1['total_cost']:
        print("👉 Вариант 2 дешевле")
    else:
        print("👉 Варианты одинаковы")