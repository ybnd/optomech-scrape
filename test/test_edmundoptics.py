import unittest
from optomech_scrape import *


class EdmundOpticsPriceRequestTest(unittest.TestCase):
    def test_iris(self):
        self.assertEqual(
            EdmundOptics.get_info('#42-123')['price'], '(!) $50.0'
        )
