#!/usr/bin/env python3
"""
Главный модуль программы "Калькулятор стоимости букета цветов".

Author: [Твое имя]
Date: 2026-03-26
"""

import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import input_output
import calculator
import logger
import model


def run_calculator():
    """Основной режим работы калькулятора."""
    try:
        input_output.show_info("Добро пожаловать в калькулятор стоимости букета!")
        logger.log_info("Программа запущена")

        while True:
            user_data = input_output.get_user_data()
            input_output.show_user_data(user_data)

            result = calculator.calculate_total(user_data)

            input_output.show_result(result)
            input_output.show_bouquet_summary(user_data, result)

            if logger.log_calculation(user_data, result):
                print(f"\n✓ Расчет сохранен в лог: {logger.get_log_path()}")

            if not input_output.confirm_action("Выполнить новый расчет?"):
                input_output.show_info("Спасибо за использование калькулятора!")
                logger.log_info("Программа завершена пользователем")
                break

            input_output.clear_screen()

    except KeyboardInterrupt:
        input_output.show_error("Программа прервана пользователем")
        logger.log_error("Программа прервана пользователем (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        input_output.show_error(f"Произошла ошибка: {e}")
        logger.log_error(str(e))
        sys.exit(1)


def optimize_bouquet():
    """
    Режим оптимизации: подбор букета под бюджет.
    """
    print("\n" + "=" * 60)
    print(" " * 15 + "ОПТИМИЗАЦИЯ БУКЕТА")
    print("=" * 60)

    try:
        # Ввод бюджета
        budget = input_output.safe_input_float("Введите ваш бюджет (руб): ", min_value=1)

        # Предпочтения
        print("\n--- ПРЕДПОЧТЕНИЯ ---")
        prefer_roses = input_output.safe_input_bool("Предпочитаете розы?", default=False)
        prefer_luxury = input_output.safe_input_bool("Предпочитаете дорогую упаковку?", default=False)
        need_delivery = input_output.safe_input_bool("Нужна доставка?", default=False)

        print("\n--- ПОИСК ОПТИМАЛЬНОГО ВАРИАНТА ---")

        # Находим оптимальный вариант
        result = model.suggest_bouquet_by_preferences(
            budget, prefer_roses, prefer_luxury, need_delivery
        )

        # Выводим результат
        print("\n" + "=" * 60)
        print(" " * 15 + "РЕКОМЕНДУЕМЫЙ БУКЕТ")
        print("=" * 60)

        print(f"\n  Цветы: {result['flower_name']} - {result['quantity']} шт")
        print(f"  Упаковка: {result['packaging_name']}")
        print(f"  Доставка: {'Да' if result['delivery'] else 'Нет'}")
        print(f"  Открытка: {'Да' if result['card'] else 'Нет'}")
        print(f"  Самовывоз: {'Да' if result['self_pickup'] else 'Нет'}")

        print(f"\n  ИТОГОВАЯ СТОИМОСТЬ: {result['total_cost']:.2f} руб")
        print(f"  Остаток бюджета: {result['remaining']:.2f} руб")

        if result.get('recommended'):
            print("\n  ✓ Этот вариант подобран специально под ваши предпочтения")

        print("=" * 60 + "\n")

        # Спрашиваем, сохранить ли в лог
        if input_output.confirm_action("Сохранить этот вариант в историю?"):
            # Создаем данные для лога
            user_data = {
                'flower_type': result['flower_type'],
                'quantity': result['quantity'],
                'packaging': result['packaging_type'],
                'delivery': result['delivery'],
                'card': result['card'],
                'self_pickup': result['self_pickup']
            }

            # Пересчитываем через основной калькулятор для единообразия
            calc_result = calculator.calculate_total(user_data)
            logger.log_calculation(user_data, calc_result)
            input_output.show_success("Вариант сохранен в историю!")

    except KeyboardInterrupt:
        input_output.show_error("Оптимизация прервана")
    except Exception as e:
        input_output.show_error(f"Ошибка: {e}")


def compare_bouquets():
    """
    Режим сравнения двух букетов.
    """
    print("\n" + "=" * 60)
    print(" " * 15 + "СРАВНЕНИЕ БУКЕТОВ")
    print("=" * 60)

    print("\n--- ПЕРВЫЙ БУКЕТ ---")
    user_data1 = input_output.get_user_data()
    result1 = calculator.calculate_total(user_data1)

    print("\n--- ВТОРОЙ БУКЕТ ---")
    user_data2 = input_output.get_user_data()
    result2 = calculator.calculate_total(user_data2)

    # Сравниваем
    print("\n" + "=" * 60)
    print(" " * 20 + "РЕЗУЛЬТАТ СРАВНЕНИЯ")
    print("=" * 60)

    print(f"\n  Первый букет: {result1['total_cost']:.2f} руб")
    print(f"  Второй букет: {result2['total_cost']:.2f} руб")

    diff = abs(result1['total_cost'] - result2['total_cost'])

    if result1['total_cost'] < result2['total_cost']:
        print(f"\n  ✓ Первый букет дешевле на {diff:.2f} руб")
    elif result2['total_cost'] < result1['total_cost']:
        print(f"\n  ✓ Второй букет дешевле на {diff:.2f} руб")
    else:
        print(f"\n  Букеты стоят одинаково")

    print("=" * 60 + "\n")


def show_history():
    """Показывает историю расчетов из лога."""
    history = logger.get_history()

    if not history:
        input_output.show_info("История расчетов пуста")
        return

    print("\n" + "=" * 60)
    print(" " * 20 + "ИСТОРИЯ РАСЧЕТОВ")
    print("=" * 60)

    for i, entry in enumerate(history, 1):
        print(f"\n--- ЗАПИСЬ {i} ---")
        lines = entry.split('\n')
        for line in lines[:12]:
            print(line)
        if len(lines) > 12:
            print("  ...")

    print("\n" + "=" * 60)
    input_output.wait_for_enter()


def main():
    """Главная функция программы."""
    while True:
        options = [
            "Калькулятор букета",
            "Оптимизация под бюджет",
            "Сравнить два букета",
            "Показать историю расчетов",
            "Очистить историю",
            "Выход"
        ]

        choice = input_output.show_menu(options, "КАЛЬКУЛЯТОР БУКЕТА ЦВЕТОВ")

        if choice == 1:
            run_calculator()
        elif choice == 2:
            optimize_bouquet()
        elif choice == 3:
            compare_bouquets()
        elif choice == 4:
            show_history()
        elif choice == 5:
            if input_output.confirm_action("Вы уверены, что хотите очистить историю?"):
                if logger.clear_log():
                    input_output.show_success("История очищена")
                else:
                    input_output.show_error("Ошибка при очистке истории")
        elif choice == 6:
            input_output.show_info("До свидания!")
            break


if __name__ == "__main__":
    main()