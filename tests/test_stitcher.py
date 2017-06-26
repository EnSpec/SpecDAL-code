import unittest
import os
import sys
import pandas as pd
import pandas.util.testing as pdt

sys.path.insert(0, os.path.abspath(".."))
from specdal import spectrum as s
from specdal import stitchers as st


class StitcherTests(unittest.TestCase):
    def setUp(self):
        self.s1 = s.Spectrum(name="s1", resampled=True)  # one sequence
        self.s2 = s.Spectrum(name="s2", resampled=True)  # three sequences

        # create test case
        self.s1.data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0],
                                     "pct_reflect": [1.0, 2.0, 3.0, 4.0]})
        self.s1.data = self.s1.data.set_index("wave")

        self.s2.data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0,
                                              2.0, 3.0, 4.0, 5.0, 6.0, 7.0,
                                              5.0, 6.0, 7.0, 8.0],
                                     "pct_reflect": [1.0, 2.0, 3.0, 4.0,
                                                     5.5, 6.5, 7.5, 8.5, 9.5, 10.5,
                                                     11.0, 12.0, 13.0, 14.0]})
        self.s2.data = self.s2.data.set_index("wave")

        # stitch test case
        self.s1 = st.stitch(self.s1)
        self.s2 = st.stitch(self.s2)

        # stitched data for validation
        self.s1_st_data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0],
                                        "pct_reflect": [1.0, 2.0, 3.0, 4.0]})
        self.s1_st_data = self.s1_st_data.set_index("wave")

        self.s2_st_data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0,
                                                 5.0, 6.0, 7.0, 8.0],
                                        "pct_reflect": [1.0, 3.75, 4.75, 5.75,
                                                        9.75, 10.75, 11.75, 14.0]})
        self.s2_st_data = self.s2_st_data.set_index("wave")

    def test_mean_stitcher_index1(self):
        pdt.assert_index_equal(self.s1.data.index,
                               self.s1_st_data.index)

    def test_mean_stitcher_data1(self):
        pdt.assert_frame_equal(self.s1.data, self.s1_st_data)

    def test_mean_stitcher_index2(self):
        pdt.assert_index_equal(self.s2.data.index,
                               self.s2_st_data.index)

    def test_mean_stitcher_data2(self):
        pdt.assert_frame_equal(self.s2.data, self.s2_st_data)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
