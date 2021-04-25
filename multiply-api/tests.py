import unittest
from unittest.mock import Mock, patch, MagicMock
from services import NumberService, ApiService
from datetime import datetime


class NumberServiceTest(unittest.TestCase):
    def test_save(self):
        with patch("models.Number") as Number:
            Number.save = MagicMock('save')
            number_service = NumberService()
            data = {
                "number": 344555,
                "timestamp": datetime.now().timestamp()
            }
            number_service.save(data)
            Number.save.assert_called_with(data)


if __name__ == '__main__':
    unittest.main()