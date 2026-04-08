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

            # ===== ОДНА ФУНКЦИЯ ВМЕСТО МНОГИХ =====
            result = calculator.calculate_total(user_data)
            # =====================================

            # Выводим результат
            input_output.show_result(result)

            # Показываем сводку
            input_output.show_bouquet_summary(user_data, result)

            # Логируем расчет
            if logger.log_calculation(user_data, result):
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
        for line in lines[:12]:  # Показываем первые 12 строк
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