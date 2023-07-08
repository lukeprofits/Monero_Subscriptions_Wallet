import unittest
from src.utils import valid_address, make_payment_id
class UtilsTest(unittest.TestCase):
    def test_valid_address(self):
        test_address = "488tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H"
        self.assertEqual(valid_address(test_address), True)
        invalid_address = "888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H"
        self.assertEqual(valid_address(invalid_address), False)
