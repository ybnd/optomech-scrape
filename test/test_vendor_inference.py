import unittest
from optomech_scrape import *


class InferVendorPriceRequestTest(unittest.TestCase):
    def test_stage(self):
        _, _, info, _ = parse('Thorlabs LNR25ZFS-M')
        self.assertEqual(
            info['price'], '€1612.03'
        )

    def test_xy(self):
        _, _, info, _ = parse('EdmundOptics #89-364')
        self.assertEqual(
            info['price'], '(!) $5500.0'
        )
