"""
Модульные тесты для calculator.py

Запуск: pytest tests/test_calculator.py -v
"""

import unittest
import sys
import os

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import calculator


class TestCalculatorBase(unittest.TestCase):
    """Тесты для базовых функций calculator.py"""

    def test_calculate_base_cost_valid(self):
        """Тест корректного расчета базовой стоимости"""
        # Розы: 150 * 10 = 1500
        self.assertEqual(calculator.calculate_base_cost(1, 10), 1500.0)

        # Тюльпаны: 80 * 5 = 400
        self.assertEqual(calculator.calculate_base_cost(2, 5), 400.0)

        # Хризантемы: 100 * 3 = 300
        self.assertEqual(calculator.calculate_base_cost(3, 3), 300.0)

    def test_calculate_base_cost_zero_quantity(self):
        """Тест на количество цветов = 0"""
        with self.assertRaises(ValueError):
            calculator.calculate_base_cost(1, 0)

    def test_calculate_base_cost_negative_quantity(self):
        """Тест на отрицательное количество цветов"""
        with self.assertRaises(ValueError):
            calculator.calculate_base_cost(1, -5)

    def test_calculate_base_cost_invalid_flower_type(self):
        """Тест на неверный тип цветов"""
        with self.assertRaises(ValueError):
            calculator.calculate_base_cost(99, 10)

    def test_calculate_base_cost_large_quantity(self):
        """Тест на большое количество цветов"""
        result = calculator.calculate_base_cost(1, 1000)
        self.assertEqual(result, 150000.0)

    def test_calculate_packaging_cost_valid(self):
        """Тест корректного расчета стоимости упаковки"""
        self.assertEqual(calculator.calculate_packaging_cost(1), 50.0)
        self.assertEqual(calculator.calculate_packaging_cost(2), 100.0)
        self.assertEqual(calculator.calculate_packaging_cost(3), 200.0)

    def test_calculate_packaging_cost_invalid(self):
        """Тест на неверный тип упаковки"""
        with self.assertRaises(ValueError):
            calculator.calculate_packaging_cost(99)

    def test_calculate_services_cost_only_delivery(self):
        """Тест: только доставка"""
        result = calculator.calculate_services_cost(True, False)
        self.assertEqual(result, 300.0)

    def test_calculate_services_cost_only_card(self):
        """Тест: только открытка"""
        result = calculator.calculate_services_cost(False, True)
        self.assertEqual(result, 50.0)

    def test_calculate_services_cost_both(self):
        """Тест: доставка и открытка"""
        result = calculator.calculate_services_cost(True, True)
        self.assertEqual(result, 350.0)

    def test_calculate_services_cost_none(self):
        """Тест: без услуг"""
        result = calculator.calculate_services_cost(False, False)
        self.assertEqual(result, 0.0)

    def test_calculate_subtotal_valid(self):
        """Тест корректного расчета промежуточной суммы"""
        # 10 роз (1500) + лента (50) + доставка (300) = 1850
        subtotal = calculator.calculate_subtotal(1, 10, 1, True, False)
        self.assertEqual(subtotal, 1850.0)

    def test_get_flower_name(self):
        """Тест получения названия цветов"""
        self.assertEqual(calculator.get_flower_name(1), "Розы")
        self.assertEqual(calculator.get_flower_name(2), "Тюльпаны")
        self.assertEqual(calculator.get_flower_name(3), "Хризантемы")

    def test_get_packaging_name(self):
        """Тест получения названия упаковки"""
        self.assertEqual(calculator.get_packaging_name(1), "Лента")
        self.assertEqual(calculator.get_packaging_name(2), "Бумага")
        self.assertEqual(calculator.get_packaging_name(3), "Корзина")

    def test_get_flower_price(self):
        """Тест получения цены цветка"""
        self.assertEqual(calculator.get_flower_price(1), 150.0)
        self.assertEqual(calculator.get_flower_price(2), 80.0)
        self.assertEqual(calculator.get_flower_price(3), 100.0)

    def test_calculate_full_price_valid(self):
        """Тест полного расчета"""
        user_data = {
            'flower_type': 1,
            'quantity': 10,
            'packaging': 2,
            'delivery': True,
            'card': True
        }
        result = calculator.calculate_full_price(user_data)

        # Проверяем структуру результата
        self.assertIn('base_cost', result)
        self.assertIn('packaging_cost', result)
        self.assertIn('services_cost', result)
        self.assertIn('subtotal', result)

        # Проверяем значения
        self.assertEqual(result['base_cost'], 1500.0)
        self.assertEqual(result['packaging_cost'], 100.0)
        self.assertEqual(result['services_cost'], 350.0)
        self.assertEqual(result['subtotal'], 1950.0)

    def test_calculate_full_price_missing_key(self):
        """Тест на отсутствие обязательного ключа"""
        user_data = {
            'flower_type': 1,
            'quantity': 10
            # отсутствуют packaging, delivery, card
        }
        with self.assertRaises(KeyError):
            calculator.calculate_full_price(user_data)


class TestCalculatorEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев"""

    def test_minimum_quantity(self):
        """Тест: минимальное количество цветов (1)"""
        result = calculator.calculate_base_cost(1, 1)
        self.assertEqual(result, 150.0)

    def test_maximum_quantity(self):
        """Тест: максимальное количество цветов (1000)"""
        result = calculator.calculate_base_cost(2, 1000)
        self.assertEqual(result, 80000.0)

    def test_quantity_boundary(self):
        """Тест: количество чуть выше максимума"""
        with self.assertRaises(ValueError):
            calculator.calculate_base_cost(1, 1001)

    def test_all_flower_types(self):
        """Тест: все типы цветов"""
        for flower_type in [1, 2, 3]:
            result = calculator.calculate_base_cost(flower_type, 1)
            self.assertGreater(result, 0)

    def test_all_packaging_types(self):
        """Тест: все типы упаковки"""
        for packaging_type in [1, 2, 3]:
            result = calculator.calculate_packaging_cost(packaging_type)
            self.assertGreater(result, 0)


if __name__ == '__main__':
    unittest.main()