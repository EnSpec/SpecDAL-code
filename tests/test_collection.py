import unittest
import os
import sys
import pandas as pd
import pandas.util.testing as pdt
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(".."))
from specdal import spectrum as s
from specdal import collection as c
from specdal import readers as r


class CollectionTests(unittest.TestCase):
    """Relies on ~/data/specdal/Big_Bio_2014/20140611 directory with .asd files"""
    def setUp(self):
        self.c = c.Collection()
        self.bbpath = os.path.join(os.path.expanduser("~"),
                                   "data/specdal/Big_Bio_2014/20140611/")

        for f in os.listdir(self.bbpath):
            spec = r.read(os.path.join(self.bbpath, f))
            if spec is not None:
                self.c.add_spectrum(spec)

    def test_group_by_separator(self):
        for i, group in self.c.group_by_separator("_", [0, 1]):
            group.plot()
        plt.show()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
