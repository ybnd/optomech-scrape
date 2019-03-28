import unittest
from optomech import *


class ThorlabsPartNumberTest(unittest.TestCase):
    def test_fix_1(self):
        self.assertEqual(
            Thorlabs.fix('BLA-123-BLA-M'), 'BLA-123-BLA/M'
        )

    def test_fix_2(self):
        self.assertEqual(
            Thorlabs.fix('BLA-123-BLA_M'), 'BLA-123-BLA/M'
        )

    def test_valid_1(self):
        self.assertTrue(
            Thorlabs.valid_part(Thorlabs.fix('BLA-123-BLA-M'))
        )

    def test_valid_2(self):
        self.assertTrue(
            Thorlabs.valid_part(Thorlabs.fix('BLA-123-BLA'))
        )

    def test_invalid_1(self):
        self.assertFalse(
            Thorlabs.valid_part('BLA-123-BLA-M')
        )

    def test_invalid_2(self):
        self.assertFalse(
            Thorlabs.valid_part('BLA-123-bla')
        )

    def test_invalid_3(self):
        self.assertFalse(
            Thorlabs.valid_part('BLA-123-bla*')
        )

    def test_invalid_4(self):
        self.assertFalse(
            Thorlabs.valid_part('BLA_123-bla')
        )


class ThorlabsPriceRequestTest(unittest.TestCase):

    def test_tube(self):
        self.assertEqual(
            Thorlabs.get_info('SM05L10')['price'], '€13.73'
        )

    def test_cage_metric(self):
        self.assertEqual(
            Thorlabs.get_info('LCP01T-M')['price'], '€35.81'
        )

    def test_invalid(self):
        self.assertEqual(
            Thorlabs.get_info('something')['price'], None
        )

    def test_nonexistent(self):
        self.assertEqual(
            Thorlabs.get_info('SCP01T-M')['price'], None
        )


class EdmundOpticsPriceRequestTest(unittest.TestCase):
    def test_iris(self):
        self.assertEqual(
            EdmundOptics.get_info('#42-123')['price'], '(!) $50.0'
        )


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
