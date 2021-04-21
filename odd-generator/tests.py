from odd import odd
import unittest

class TestOdd(unittest.TestCase):

    def test_even_function(self):
        result = odd()
        assert result %2 != 0
        result2 = odd()
        self.assertNotEqual(result, result2)

    def test_should_be_greater_then_0(self):
        result = odd()
        self.assertGreater(result, 0)
        

    def test_should_be_less_then_1000(self):
        result = odd()
        self.assertLess(result, 1000)
        



if __name__ == "__main__":
    unittest.main()