import unittest
from src.surcharges import apply_discount


class TestSurcharges(unittest.TestCase):
    def test_discount_10_percent(self):
        self.assertEqual(apply_discount(1000, 60), 900)


if __name__ == "__main__":
    unittest.main()