import unittest
import os
import sys
import pandas as pd
import pandas.util.testing as pdt
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(".."))
from specdal.spectrum import Spectrum
from specdal.collection import Collection


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.w1 = pd.Index([1, 2, 3, 4], name="wavelength")
        self.w2 = pd.Index([2, 3, 4, 5, 6], name="wavelength")
        self.w3 = pd.Index([1, 2.3, 3.1, 4.1], name="wavelength")

        self.s1 = Spectrum(name="s_1_1",
                           measurement=pd.Series(data=[10, 20, 30, 40],
                                                 index=self.w1))
        self.s2 = Spectrum(name="s_1_2",
                           measurement=pd.Series(data=[1, 2, 3, 4, 5],
                                                 index=self.w2))
        self.s3 = Spectrum(name="s_2_1",
                           measurement=pd.Series(data=[100, 200, 300, 400],
                                                 index=self.w3))
        self.s3.resample()

        self.c = Collection(name="collection1")

        self.c.add_spectrum(self.s1)
        self.c.add_spectrum(self.s2)
        self.c.add_spectrum(self.s3)

    def test_basic(self):
        print(self.c)
        print(self.c.data)

    def test_duplicate_name(self):
        s1_dup = Spectrum(name="s_1_1")
        len_before = len(self.c.spectrums)
        self.c.add_spectrum(s1_dup)
        len_after = len(self.c.spectrums)
        self.assertEqual(len_before, len_after)

    def test_aggregate(self):
        mean = self.c.aggregate(fcn="mean")
        median = self.c.aggregate(fcn="median")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
