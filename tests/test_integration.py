"""
Интеграционные тесты для проверки работы всех модулей вместе.

Запуск: pytest tests/test_integration.py -v
"""

import unittest
import sys
import os

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import calculator
import discounts
import logger


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def setUp(self):
        """Подготовка"""
        # Очищаем лог перед тестами
        logger.clear_log()

    def test_full_calculation_delivery(self):
        """Тест: полный расчет с доставкой (без скидки)"""
        user_data = {
            'flower_type': 1,  # Розы
            'quantity': 10,  # 10 шт
            'packaging': 2,  # Бумага
            'delivery': True,  # Доставка
            'card': False,  # Без открытки
            'self_pickup': False  # Не самовывоз
        }

        result = calculator.calculate_total(user_data)

        # Проверяем расчеты
        self.assertEqual(result['base_cost'], 1500.0)  # 150 * 10
        self.assertEqual(result['packaging_cost'], 100.0)  # Бумага
        self.assertEqual(result['services_cost'], 300.0)  # Доставка
        self.assertEqual(result['subtotal'], 1900.0)  # 1500+100+300
        self.assertEqual(result['discount'], 0.0)  # Нет скидки
        self.assertEqual(result['total_cost'], 1900.0)

    def test_full_calculation_with_discount(self):
        """Тест: полный расчет со скидкой (25 цветов + самовывоз)"""
        user_data = {
            'flower_type': 1,  # Розы
            'quantity': 25,  # 25 шт (>20)
            'packaging': 1,  # Лента
            'delivery': False,  # Без доставки
            'card': True,  # С открыткой
            'self_pickup': True  # Самовывоз
        }

        result = calculator.calculate_total(user_data)

        # Базовая стоимость: 150 * 25 = 3750
        self.assertEqual(result['base_cost'], 3750.0)
        # Упаковка: лента = 50
        self.assertEqual(result['packaging_cost'], 50.0)
        # Услуги: открытка = 50
        self.assertEqual(result['services_cost'], 50.0)
        # Промежуточная: 3750+50+50 = 3850
        self.assertEqual(result['subtotal'], 3850.0)
        # Скидка: 10% от 3850 = 385
        self.assertEqual(result['discount'], 385.0)
        # Итого: 3850 - 385 = 3465
        self.assertEqual(result['total_cost'], 3465.0)

    def test_full_calculation_minimal(self):
        """Тест: минимальный заказ (1 цветок, без услуг)"""
        user_data = {
            'flower_type': 2,  # Тюльпаны
            'quantity': 1,  # 1 шт
            'packaging': 1,  # Лента
            'delivery': False,
            'card': False,
            'self_pickup': True
        }

        result = calculator.calculate_total(user_data)

        # Тюльпан: 80 руб
        self.assertEqual(result['base_cost'], 80.0)
        # Лента: 50 руб
        self.assertEqual(result['packaging_cost'], 50.0)
        # Услуг нет
        self.assertEqual(result['services_cost'], 0.0)
        # Скидка за самовывоз: 5% от 130 = 6.5
        self.assertEqual(result['discount'], 6.5)
        # Итого: 130 - 6.5 = 123.5
        self.assertEqual(result['total_cost'], 123.5)

    def test_logger_integration(self):
        """Тест: интеграция с логгером"""
        user_data = {
            'flower_type': 1,
            'quantity': 10,
            'packaging': 1,
            'delivery': False,
            'card': False,
            'self_pickup': False
        }

        result = calculator.calculate_total(user_data)

        # Логируем
        success = logger.log_calculation(user_data, result)
        self.assertTrue(success)

        # Проверяем, что лог создан
        history = logger.get_history()
        self.assertEqual(len(history), 1)

    def test_all_flower_types(self):
        """Тест: все типы цветов"""
        for flower_type in [1, 2, 3]:
            user_data = {
                'flower_type': flower_type,
                'quantity': 5,
                'packaging': 1,
                'delivery': False,
                'card': False,
                'self_pickup': True
            }

            result = calculator.calculate_total(user_data)
            self.assertGreater(result['total_cost'], 0)

    def test_all_packaging_types(self):
        """Тест: все типы упаковки"""
        for packaging in [1, 2, 3]:
            user_data = {
                'flower_type': 1,
                'quantity': 5,
                'packaging': packaging,
                'delivery': False,
                'card': False,
                'self_pickup': True
            }

            result = calculator.calculate_total(user_data)
            self.assertGreater(result['total_cost'], 0)


if __name__ == '__main__':
    unittest.main()