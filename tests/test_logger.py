"""
Модульные тесты для logger.py

Запуск: pytest tests/test_logger.py -v
"""

import unittest
import os
import sys
import tempfile

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import logger


class TestLogger(unittest.TestCase):
    """Тесты для модуля логирования"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        # Создаем временный файл для лога
        self.temp_dir = tempfile.mkdtemp()
        self.test_log_file = os.path.join(self.temp_dir, "test.log")

        # Создаем временный логгер
        self.test_logger = logger.BouquetLogger(self.test_log_file)

        # ПОЛНЫЕ данные для тестов (со всеми ключами)
        self.sample_user_data = {
            'flower_type': 1,
            'quantity': 10,
            'packaging': 1,
            'delivery': True,
            'card': False,
            'self_pickup': False
        }

        self.sample_result_data = {
            'base_cost': 1500.0,
            'packaging_cost': 50.0,
            'services_cost': 300.0,
            'subtotal': 1850.0,
            'discount': 0.0,
            'total_cost': 1850.0
        }

    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        os.rmdir(self.temp_dir)

    def test_log_creation(self):
        """Тест: создание файла лога"""
        self.test_logger.log_calculation(self.sample_user_data, self.sample_result_data)
        self.assertTrue(os.path.exists(self.test_log_file))

    def test_log_content(self):
        """Тест: содержимое лога"""
        self.test_logger.log_calculation(self.sample_user_data, self.sample_result_data)

        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("РАСЧЕТ #1", content)
        self.assertIn("Розы", content)
        self.assertIn("1850.00", content)

    def test_multiple_logs(self):
        """Тест: несколько записей в лог"""
        for i in range(3):
            user_data = self.sample_user_data.copy()
            user_data['quantity'] = i + 1
            result_data = self.sample_result_data.copy()
            result_data['base_cost'] = 150 * (i + 1)
            result_data['total_cost'] = 150 * (i + 1)
            self.test_logger.log_calculation(user_data, result_data)

        history = self.test_logger.get_history()
        self.assertEqual(len(history), 3)

    def test_get_history_limit(self):
        """Тест: получение истории с ограничением"""
        for i in range(5):
            user_data = self.sample_user_data.copy()
            user_data['quantity'] = i + 1
            result_data = self.sample_result_data.copy()
            result_data['base_cost'] = 150 * (i + 1)
            result_data['total_cost'] = 150 * (i + 1)
            self.test_logger.log_calculation(user_data, result_data)

        history = self.test_logger.get_history(limit=2)
        self.assertEqual(len(history), 2)

    def test_clear_log(self):
        """Тест: очистка лога"""
        self.test_logger.log_calculation(self.sample_user_data, self.sample_result_data)
        self.assertTrue(os.path.exists(self.test_log_file))

        # Проверяем, что файл не пустой
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertNotEqual(content, "")

        # Очищаем
        self.test_logger.clear_log()

        # После очистки файл должен быть пустым
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "")

    def test_log_error(self):
        """Тест: запись ошибки в лог"""
        self.test_logger.log_error("Test error message")

        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("ОШИБКА", content)
        self.assertIn("Test error message", content)

    def test_log_info(self):
        """Тест: запись информационного сообщения"""
        self.test_logger.log_info("Test info message")

        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("INFO:", content)
        self.assertIn("Test info message", content)

    def test_get_log_path(self):
        """Тест: получение пути к логу"""
        path = self.test_logger.get_log_path()
        self.assertEqual(path, os.path.abspath(self.test_log_file))

    def test_get_log_size(self):
        """Тест: получение размера лога"""
        self.test_logger.log_calculation(self.sample_user_data, self.sample_result_data)

        size = self.test_logger.get_log_size()
        self.assertGreater(size, 0)

    def test_log_with_missing_keys(self):
        """Тест: логгер не падает при отсутствии ключей"""
        # Неполные данные
        incomplete_data = {'flower_type': 1, 'quantity': 10}
        incomplete_result = {'total_cost': 1000}

        # Должен не упасть, а записать в лог
        result = self.test_logger.log_calculation(incomplete_data, incomplete_result)
        self.assertTrue(result)


class TestGlobalLogger(unittest.TestCase):
    """Тесты для глобальных функций логгера"""

    def test_global_logger_singleton(self):
        """Тест: глобальный логгер - синглтон"""
        logger1 = logger.get_logger()
        logger2 = logger.get_logger()

        self.assertIs(logger1, logger2)


if __name__ == '__main__':
    unittest.main()