import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(".."))
from specdal.spectrum import Spectrum
import pandas as pd
import pandas.util.testing as pdt


class SpectrumTests(unittest.TestCase):
    def setUp(self):
        self.w1 = pd.Index([1, 2, 3, 4], name="wavelength")
        self.w2 = pd.Index([2, 3, 4, 5, 6], name="wavelength")
        self.s1 = Spectrum(name="s1",
                           reflectance=pd.Series(data=[10, 20, 30, 40],
                                                 index=self.w1,
                                                 name="reflectance"))
        self.s2 = Spectrum(name="s2",
                           reflectance=pd.Series(data=[10, 10, 20, 30],
                                                 index=self.w1,
                                                 name="reflectance"))

        self.s3 = Spectrum(name="s3",
                           reflectance=pd.Series(data=[10, 10, 20, 30, 40],
                                                 index=self.w2,
                                                 name="reflectance"))

    def test_addition_sameIndex(self):
        s1_add_s2 = self.s1 + self.s2
        pdt.assert_series_equal(s1_add_s2,
                                pd.Series(data=[20, 30, 50, 70],
                                          index=self.w1,
                                          name="reflectance"))

    def test_addition_diffIndex(self):
        s1_add_s3 = self.s1 + self.s3
        pdt.assert_series_equal(s1_add_s3,
                                pd.Series(data=[10, 30, 40, 60, 30, 40],
                                          index=pd.Index([1, 2, 3, 4, 5, 6],
                                                         name="wavelength"),
                                          name="reflectance"))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
