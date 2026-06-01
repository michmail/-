"""
Модуль ввода/вывода данных.
"""

from typing import Dict


def get_flower_type() -> int:
    print("\nВыберите тип цветов:")
    print("1 - Розы (150 руб/шт)")
    print("2 - Тюльпаны (80 руб/шт)")
    print("3 - Хризантемы (100 руб/шт)")
    while True:
        try:
            choice = int(input("Ваш выбор (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            print("Ошибка: введите 1, 2 или 3")
        except ValueError:
            print("Ошибка: введите целое число")


def get_quantity() -> int:
    while True:
        try:
            qty = int(input("Введите количество цветов: "))
            if qty > 0:
                return qty
            print("Ошибка: количество должно быть > 0")
        except ValueError:
            print("Ошибка: введите целое число")


def get_packaging_type() -> int:
    print("\nВыберите тип упаковки:")
    print("1 - Лента (50 руб)")
    print("2 - Бумага (100 руб)")
    print("3 - Корзина (200 руб)")
    while True:
        try:
            choice = int(input("Ваш выбор (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            print("Ошибка: введите 1, 2 или 3")
        except ValueError:
            print("Ошибка: введите целое число")


def get_delivery() -> bool:
    while True:
        answer = input("Нужна доставка? (да/нет): ").lower().strip()
        if answer in ["да", "yes", "y", "1"]:
            return True
        if answer in ["нет", "no", "n", "0"]:
            return False
        print("Ошибка: введите 'да' или 'нет'")


def get_card() -> bool:
    while True:
        answer = input("Нужна открытка? (да/нет): ").lower().strip()
        if answer in ["да", "yes", "y", "1"]:
            return True
        if answer in ["нет", "no", "n", "0"]:
            return False
        print("Ошибка: введите 'да' или 'нет'")


def print_result(result: Dict) -> None:
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТ РАСЧЁТА БУКЕТА")
    print("=" * 40)
    print(f"Цветы: {result['flower_name']} x {result['quantity']} шт")
    print(f"Стоимость цветов: {result['base_cost']} руб")
    print(f"Упаковка: {result['packaging_name']} - {result['packaging_cost']} руб")
    print(f"Доставка: {'Да' if result['delivery'] else 'Нет'}")
    print(f"Открытка: {'Да' if result['card'] else 'Нет'}")
    print(f"Услуги: {result['services_cost']} руб")
    print("-" * 40)
    print(f"ИТОГО: {result['total_cost']} руб")
    print("=" * 40)