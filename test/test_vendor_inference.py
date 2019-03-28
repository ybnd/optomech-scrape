import unittest
from optomech_scrape import *


class InferVendorPriceRequestTest(unittest.TestCase):
    def test_stage(self):
        _, _, info, _ = part('Thorlabs LNR25ZFS-M')
        self.assertEqual(
            info['price'], '€1612.03'
        )

    def test_xy(self):
        _, _, info, _ = part('EdmundOptics #89-364')
        self.assertEqual(
            info['price'], '(!) $5500.0'
        )
