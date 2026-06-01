"""
Модульные тесты для discounts.py

Запуск: pytest tests/test_discounts.py -v
"""

import unittest
import sys
import os

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import discounts


class TestDiscountsBasic(unittest.TestCase):
    """Тесты для базовых скидок"""

    def test_discount_quantity_only(self):
        """Тест: только скидка за количество (>20)"""
        # 25 цветов, доставка, сумма 1000
        discount = discounts.calculate_discount(25, False, 1000)
        self.assertEqual(discount, 50.0)  # 5% от 1000

    def test_discount_self_pickup_only(self):
        """Тест: только скидка за самовывоз"""
        # 10 цветов, самовывоз, сумма 1000
        discount = discounts.calculate_discount(10, True, 1000)
        self.assertEqual(discount, 50.0)  # 5% от 1000

    def test_discount_both(self):
        """Тест: обе скидки (количество + самовывоз)"""
        # 25 цветов, самовывоз, сумма 1000
        discount = discounts.calculate_discount(25, True, 1000)
        self.assertEqual(discount, 100.0)  # 10% от 1000

    def test_discount_none(self):
        """Тест: без скидок"""
        # 10 цветов, доставка, сумма 1000
        discount = discounts.calculate_discount(10, False, 1000)
        self.assertEqual(discount, 0.0)

    def test_discount_max_limit(self):
        """Тест: максимальная скидка не более 10%"""
        # 25 цветов + самовывоз = 10% (максимум)
        discount = discounts.calculate_discount(25, True, 1000)
        self.assertEqual(discount, 100.0)

        # Даже если добавить еще условия, больше 10% не будет
        discount = discounts.calculate_discount(25, True, 1000, flower_type=1, repeat_customer=True)
        self.assertLessEqual(discount, 100.0)  # не более 10% от 1000


class TestDiscountRate(unittest.TestCase):
    """Тесты для получения процента скидки"""

    def test_discount_rate_none(self):
        """Тест: процент без скидок"""
        rate = discounts.get_discount_rate(10, False)
        self.assertEqual(rate, 0.0)

    def test_discount_rate_quantity(self):
        """Тест: процент за количество"""
        rate = discounts.get_discount_rate(25, False)
        self.assertEqual(rate, 0.05)

    def test_discount_rate_self_pickup(self):
        """Тест: процент за самовывоз"""
        rate = discounts.get_discount_rate(10, True)
        self.assertEqual(rate, 0.05)

    def test_discount_rate_both(self):
        """Тест: процент за обе скидки"""
        rate = discounts.get_discount_rate(25, True)
        self.assertEqual(rate, 0.10)


class TestBulkDiscount(unittest.TestCase):
    """Тесты для оптовой скидки"""

    def test_bulk_discount_50(self):
        """Тест: 50+ цветов - скидка 5%"""
        discount = discounts.calculate_bulk_discount(50, 100)
        # 50 * 100 = 5000, 5% = 250
        self.assertEqual(discount, 250.0)

    def test_bulk_discount_100(self):
        """Тест: 100+ цветов - скидка 10%"""
        discount = discounts.calculate_bulk_discount(100, 100)
        # 100 * 100 = 10000, 10% = 1000
        self.assertEqual(discount, 1000.0)

    def test_bulk_discount_200(self):
        """Тест: 200+ цветов - скидка 15%"""
        discount = discounts.calculate_bulk_discount(200, 100)
        # 200 * 100 = 20000, 15% = 3000
        self.assertEqual(discount, 3000.0)

    def test_bulk_discount_none(self):
        """Тест: меньше 50 цветов - без скидки"""
        discount = discounts.calculate_bulk_discount(49, 100)
        self.assertEqual(discount, 0.0)


class TestLoyaltyDiscount(unittest.TestCase):
    """Тесты для скидки постоянным клиентам"""

    def test_loyalty_5_orders(self):
        """Тест: 5 заказов - скидка 3%"""
        rate = discounts.calculate_loyalty_discount(5)
        self.assertEqual(rate, 0.03)

    def test_loyalty_10_orders(self):
        """Тест: 10 заказов - скидка 5%"""
        rate = discounts.calculate_loyalty_discount(10)
        self.assertEqual(rate, 0.05)

    def test_loyalty_25_orders(self):
        """Тест: 25 заказов - скидка 10%"""
        rate = discounts.calculate_loyalty_discount(25)
        self.assertEqual(rate, 0.10)

    def test_loyalty_no_discount(self):
        """Тест: меньше 5 заказов - без скидки"""
        rate = discounts.calculate_loyalty_discount(4)
        self.assertEqual(rate, 0.0)


class TestPromoDiscount(unittest.TestCase):
    """Тесты для скидок по промокоду"""

    def test_promo_flower10(self):
        """Тест: промокод FLOWER10 - 10%"""
        discount = discounts.calculate_promo_discount("FLOWER10", 1000)
        self.assertEqual(discount, 100.0)

    def test_promo_welcome5(self):
        """Тест: промокод WELCOME5 - 5%"""
        discount = discounts.calculate_promo_discount("WELCOME5", 1000)
        self.assertEqual(discount, 50.0)

    def test_promo_love15_with_limit(self):
        """Тест: промокод LOVE15 - 15% но не более 500"""
        # Сумма 1000: 15% = 150 (меньше 500)
        discount = discounts.calculate_promo_discount("LOVE15", 1000)
        self.assertEqual(discount, 150.0)

        # Сумма 5000: 15% = 750 (ограничивается 500)
        discount = discounts.calculate_promo_discount("LOVE15", 5000)
        self.assertEqual(discount, 500.0)

    def test_promo_invalid(self):
        """Тест: неверный промокод"""
        discount = discounts.calculate_promo_discount("INVALID", 1000)
        self.assertEqual(discount, 0.0)

    def test_promo_case_insensitive(self):
        """Тест: промокод нечувствителен к регистру"""
        discount1 = discounts.calculate_promo_discount("flower10", 1000)
        discount2 = discounts.calculate_promo_discount("FLOWER10", 1000)
        self.assertEqual(discount1, discount2)


class TestCanApplyDiscount(unittest.TestCase):
    """Тесты для проверки возможности скидки"""

    def test_can_apply_both(self):
        """Тест: можно применить скидку (количество >20 и самовывоз)"""
        self.assertTrue(discounts.can_apply_discount(25, True))

    def test_can_apply_quantity_only(self):
        """Тест: можно применить скидку (только количество)"""
        self.assertTrue(discounts.can_apply_discount(25, False))

    def test_can_apply_self_pickup_only(self):
        """Тест: можно применить скидку (только самовывоз)"""
        self.assertTrue(discounts.can_apply_discount(10, True))

    def test_cannot_apply(self):
        """Тест: нельзя применить скидку"""
        self.assertFalse(discounts.can_apply_discount(10, False))


class TestTotalDiscount(unittest.TestCase):
    """Тесты для общей суммы всех скидок"""

    def test_total_discount_basic(self):
        """Тест: базовая скидка"""
        result = discounts.calculate_total_discount(25, True, 1000)
        self.assertEqual(result['standard_discount'], 100.0)
        self.assertEqual(result['total_discount'], 100.0)

    def test_total_discount_with_promo(self):
        """Тест: скидка + промокод"""
        result = discounts.calculate_total_discount(
            25, True, 1000, promo_code="FLOWER10"
        )
        # Стандартная 10% (100) + промо 10% (100) = 200
        self.assertEqual(result['total_discount'], 200.0)

    def test_total_discount_max_limit(self):
        """Тест: максимальная общая скидка 30%"""
        # Слишком много скидок, должно ограничиться 30%
        result = discounts.calculate_total_discount(
            25, True, 1000,
            flower_type=1,
            repeat_customer=True,
            promo_code="LOVE15"
        )
        # Максимум 30% от 1000 = 300
        self.assertLessEqual(result['total_discount'], 300.0)


if __name__ == '__main__':
    unittest.main()