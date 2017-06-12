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
        # total 36 spectra
        self.c = Collection(name="For Groups")
        for a in ("A", "B", "C"):
            for b in ("a", "b", "c"):
                for c in ("0001", "0002", "0003", "0004"):
                    self.c.add_spectrum(Spectrum("_".join([a, b, c])))

    def test_num_groups(self):
        groups = self.c.group_by(separator="_", indices=[0])
        self.assertEqual(len(groups), 3)

        groups = self.c.group_by(separator="_", indices=[1])
        self.assertEqual(len(groups), 3)
        
        groups = self.c.group_by(separator="_", indices=[2])
        self.assertEqual(len(groups), 4)
        
        groups = self.c.group_by(separator="_", indices=[0, 1])
        self.assertEqual(len(groups), 9)

        groups = self.c.group_by(separator="_", indices=[0, 2])
        self.assertEqual(len(groups), 12)

        groups = self.c.group_by(separator="_", indices=[1, 2])
        self.assertEqual(len(groups), 12)

        groups = self.c.group_by(separator="_", indices=[0, 1, 2])
        self.assertEqual(len(groups), 36)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
