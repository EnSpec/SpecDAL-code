import unittest
import os
import sys
import pandas as pd
import pandas.util.testing as pdt
import numpy as np

sys.path.insert(0, os.path.abspath(".."))
from specdal import spectrum as s
from specdal import resamplers as rs


class ResamplerTests(unittest.TestCase):
    def setUp(self):
        self.s1 = s.Spectrum(name="s1")  # one sequence
        self.s2 = s.Spectrum(name="s2")  # three sequences

        # create test case
        self.s1.data = pd.DataFrame({"wave": [1.2, 2, 2.8, 4],
                                     "pct_reflect": [1, 2, 3, 4]})
        self.s1.data = self.s1.data.set_index("wave")

        self.s2.data = pd.DataFrame({"wave": [1.2, 1.9, 2.8, 4, 2.2,
                                              3.1, 4.2, 5.1, 5.9, 6.2,
                                              4.9, 6.1, 7, 8.1],
                                     "pct_reflect": [1, 2, 3,
                                                     4, 5, 6, 7, 8, 9, 10,
                                                     11, 12, 13, 14]})
        self.s2.data = self.s2.data.set_index("wave")

        # resampled data for validation
        self.valid1 = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0],
                                        "pct_reflect": [1, 2, 3, 4]}) # replace with correct values
        self.valid1 = self.valid1.set_index("wave")

    def test_linear_resampler(self):
        self.assertFalse(self.s1.resampled)
        s1_rs = rs.resample(self.s1)
        self.assertTrue(s1_rs.resampled)

        print(s1_rs.data)
        # check index
        pdt.assert_index_equal(s1_rs.data.index,
                               self.valid1.index)

        # check data
        #pdt.assert_frame_equal(s1_rs.data, pd.DataFrame())  # replace with reampled values


def main():
    unittest.main()


if __name__ == '__main__':
    main()
