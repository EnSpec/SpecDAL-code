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
        self.w3 = pd.Index([5.1, 5.9, 7.0, 8.1], name="wavelength")

        self.s1 = Spectrum(name="s1",
                           measurement=pd.Series(data=[10, 20, 30, 40],
                                                 index=self.w1))
        self.s2 = Spectrum(name="s2",
                           measurement=pd.Series(data=[10, 10, 20, 30],
                                                 index=self.w1))

        self.s3 = Spectrum(name="s3",
                           measurement=pd.Series(data=[10, 10, 20, 30, 40],
                                                 index=self.w2))

    def test_members(self):
        print(self.s1)
        print(self.s1.name)
        print(self.s1.measurement)

    def test_addition_sameIndex(self):
        s1_add_s2 = self.s1 + self.s2
        s1_add_s2_answer = pd.Series(data=[20, 30, 50, 70], index=self.w1)
        s1_add_s2_answer.name = "pct_reflect"
        pdt.assert_series_equal(s1_add_s2, s1_add_s2_answer)
    
    def test_addition_diffIndex(self):
        s1_add_s3 = self.s1 + self.s3
        s1_add_s3_answer = pd.Series(data=[10, 30, 40, 60, 30, 40],
                                     index=pd.Index([1, 2, 3, 4, 5, 6],
                                                    name="wavelength"))
        s1_add_s3_answer.name = "pct_reflect"
        pdt.assert_series_equal(s1_add_s3, s1_add_s3_answer)

    def test_resample(self):
        # change index to non-integer wavelengths
        self.s1.measurement.index = self.w3
        self.s1.resample()
        index_answer = pd.Index([6.0, 7.0, 8.0], name="wavelength")
        pdt.assert_index_equal(self.s1.measurement.index, index_answer)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
