"""
Главный модуль программы "Калькулятор стоимости букета цветов".
Временная версия для тестирования модуля ввода/вывода.
"""

import input_output

def main():
    """
    Главная функция программы.
    """
    print("Запуск калькулятора стоимости букета цветов")

    # Запрашиваем данные у пользователя
    user_data = input_output.get_user_data()

    # Показываем, какие данные ввел пользователь (для проверки)
    print("\n" + "="*50)
    print("ВВЕДЕННЫЕ ДАННЫЕ")
    print("="*50)
    print(f"Тип цветов: {user_data['flower_type']}")
    print(f"Количество: {user_data['quantity']} шт")
    print(f"Упаковка: {user_data['packaging']}")
    print(f"Доставка: {'Да' if user_data['delivery'] else 'Нет'}")
    print(f"Открытка: {'Да' if user_data['card'] else 'Нет'}")
    print(f"Самовывоз: {'Да' if user_data['self_pickup'] else 'Нет'}")

    # Временные данные для демонстрации вывода
    # Позже здесь будет реальный расчет
    test_result = {
        'base_cost': 1000.00,
        'packaging_cost': 100.00,
        'services_cost': 300.00,
        'discount': 50.00,
        'total_cost': 1350.00
    }

    # Выводим результат
    input_output.show_result(test_result)

    print("\nПрограмма завершена. Спасибо за использование!")

if __name__ == "__main__":
    main()