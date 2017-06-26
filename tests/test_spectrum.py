import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(".."))
from specdal import spectrum
import pandas as pd

class SpectrumTests(unittest.TestCase):
    def setUp(self):
        self.s = spectrum.Spectrum("a")

    def testName(self):
        # initial name
        self.assertEqual(self.s.name, "a")

    def testNameChange(self):
        # change name
        s = spectrum.Spectrum("a")
        self.s.name = "abc_def"
        self.assertEqual(self.s.name, "abc_def")

    def testData(self):
        self.s.data = pd.DataFrame({"wave": [1.2, 1.9, 2.8, 4, 2.2,
                                             3.1, 4.2, 5.1, 5.9, 6.2,
                                             4.9, 6.1, 7, 8.1],
                                    "pct_reflect": [1, 2, 3,
                                                    4, 5, 6, 7, 8, 9, 10,
                                                    11, 12, 13, 14]})
        self.s.data = self.s.data.set_index("wave")
        

def main():
    unittest.main()


if __name__ == '__main__':
    main()
