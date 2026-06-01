import unittest
from src.calculator import calculate_base_cost, calculate_packaging_cost


class TestCalculator(unittest.TestCase):
    def test_base_cost_roses(self):
        self.assertEqual(calculate_base_cost(1, 10), 1500)


if __name__ == "__main__":
    unittest.main()