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
import discounts
import logger


def run_calculator():
    """Основной режим работы калькулятора."""
    try:
        input_output.show_info("Добро пожаловать в калькулятор стоимости букета!")
        logger.log_info("Программа запущена")

        while True:
            # Запрашиваем данные
            user_data = input_output.get_user_data()

            # Показываем введенные данные
            input_output.show_user_data(user_data)

            # Расчет базовой стоимости
            base_cost = calculator.calculate_base_cost(
                user_data['flower_type'],
                user_data['quantity']
            )

            # Расчет стоимости упаковки
            packaging_cost = calculator.calculate_packaging_cost(
                user_data['packaging']
            )

            # Расчет стоимости услуг
            services_cost = calculator.calculate_services_cost(
                user_data['delivery'],
                user_data['card']
            )

            # Промежуточная сумма
            subtotal = base_cost + packaging_cost + services_cost

            print("\n--- РАСЧЕТ СКИДОК ---")

            # Расчет скидки
            discount_amount = discounts.calculate_discount(
                user_data['quantity'],
                user_data['self_pickup'],
                subtotal,
                flower_type=user_data['flower_type']
            )

            # Итоговая стоимость
            total_cost = subtotal - discount_amount

            # Формируем результат
            result_data = {
                'base_cost': base_cost,
                'packaging_cost': packaging_cost,
                'services_cost': services_cost,
                'subtotal': subtotal,
                'discount': discount_amount,
                'total_cost': total_cost
            }

            # Выводим результат
            input_output.show_result(result_data)

            # Показываем сводку
            input_output.show_bouquet_summary(user_data, result_data)

            # Логируем расчет
            if logger.log_calculation(user_data, result_data):
                print(f"\n✓ Расчет сохранен в лог: {logger.get_log_path()}")
            else:
                print("\n✗ Ошибка при сохранении лога")

            # Спрашиваем о продолжении
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
        # Показываем только первые строки каждой записи
        lines = entry.split('\n')
        for line in lines[:10]:  # Показываем первые 10 строк
            print(line)
        if len(lines) > 10:
            print("  ...")

    print("\n" + "=" * 60)
    input_output.wait_for_enter()


def main():
    """Главная функция программы."""
    while True:
        options = [
            "Калькулятор букета",
            "Показать историю расчетов",
            "Очистить историю",
            "Выход"
        ]

        choice = input_output.show_menu(options, "КАЛЬКУЛЯТОР БУКЕТА ЦВЕТОВ")

        if choice == 1:
            run_calculator()
        elif choice == 2:
            show_history()
        elif choice == 3:
            if input_output.confirm_action("Вы уверены, что хотите очистить историю?"):
                if logger.clear_log():
                    input_output.show_success("История очищена")
                else:
                    input_output.show_error("Ошибка при очистке истории")
        elif choice == 4:
            input_output.show_info("До свидания!")
            break


if __name__ == "__main__":
    main()