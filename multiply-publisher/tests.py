import unittest
from unittest.mock import Mock, patch, MagicMock
from multiply import Multiply, INumberDTO


class TestMultiply(unittest.TestCase):

    def test_multiply(self):
        with patch('multiply.MultiplyService') as mock:
            multiply_service = mock.return_value
            multiply_service.get_service_number.return_value = INumberDTO(2, 2342234234)
            multiply = Multiply("/even", "/odd", multiply_service)
            self.assertEqual(multiply.multiply(), 4)

    def test_if_publish_number(self):
        with patch('multiply.MultiplyService') as mock:
            multiply_service = mock.return_value
            multiply_service.get_service_number.return_value = INumberDTO(200, 2342234234)
            multiply_service.publish = MagicMock(name="publish")
            multiply = Multiply("/even", "/odd", multiply_service)
            multiply.publisher()
            multiply_service.publish.assert_called_once_with(40000)

    def test_if_not_publish_number(self):
        with patch('multiply.MultiplyService') as mock:
            multiply_service = mock.return_value
            multiply_service.get_service_number.return_value = INumberDTO(2, 2342234234)
            multiply_service.publish = MagicMock(name="publish")
            multiply = Multiply("/even", "/odd", multiply_service)
            multiply.publisher()
            multiply_service.publish.assert_not_called()


if __name__ == '__main__':
    unittest.main()