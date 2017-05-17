import unittest
import os
import sys
import pandas as pd
import pandas.util.testing as pdt
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(".."))
from specdal import spectrum as s


class StitcherTests(unittest.TestCase):
    # def test_jump_correction1(self):
    #     s1 = s.Spectrum(name="s1", resampled=True)  # one sequence
    #     print(s1)
    #     
    #     # create test case
    #     s1.data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0,
    #                                           5.0, 6.0, 7.0, 8.0],
    #                                  "pct_reflect": [1.0, 2.0, 3.0, 4.0,
    #                                                  10.0, 11.0, 12.0, 13.0]})
    #     s1.data = s1.data.set_index("wave")
    #     s1.data.plot(y='pct_reflect')
    #     plt.show()
    #     s1.stitch(method='jump', waves=[4], reference=0)
    #     s1.data.plot(y='pct_reflect')
    #     plt.show()
        

    def test_jump_correction2(self):        
        s2 = s.Spectrum(name="s2", resampled=True)  # two sequence
        s2.data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0,
                                              5.0, 6.0, 7.0, 8.0,
                                              9.0, 10.0, 11.0, 12.0],
                                     "pct_reflect": [1.0, 2.0, 3.0, 4.0,
                                                     10.0, 11.0, 12.0, 13.0,
                                                     8.0, 9.0, 10.0, 11.0]})
        s2.data = s2.data.set_index("wave")
        s2.data.plot(y='pct_reflect')
        s2.stitch(method='jump', waves=[4, 8], reference=0)
        s2.data.plot(y='pct_reflect')

#         # stitched data for validation
#         self.s1_st_data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0],
#                                         "pct_reflect": [1.0, 2.0, 3.0, 4.0]})
#         self.s1_st_data = self.s1_st_data.set_index("wave")
# 
#         self.s2_st_data = pd.DataFrame({"wave": [1.0, 2.0, 3.0, 4.0,
#                                                  5.0, 6.0, 7.0, 8.0],
#                                         "pct_reflect": [1.0, 3.75, 4.75, 5.75,
#                                                         9.75, 10.75, 11.75, 14.0]})
#         self.s2_st_data = self.s2_st_data.set_index("wave")
# 
#     def test_mean_stitcher_index1(self):
#         pdt.assert_index_equal(self.s1.data.index,
#                                self.s1_st_data.index)
# 
#     def test_mean_stitcher_data1(self):
#         pdt.assert_frame_equal(self.s1.data, self.s1_st_data)
# 
#     def test_mean_stitcher_index2(self):
#         pdt.assert_index_equal(self.s2.data.index,
#                                self.s2_st_data.index)
# 
#     def test_mean_stitcher_data2(self):
#         pdt.assert_frame_equal(self.s2.data, self.s2_st_data)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
