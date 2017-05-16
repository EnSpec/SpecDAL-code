import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(".."))
from specdal import readers as r

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.filepath = "../data"
        self.asdpath = "../data/asd"
        self.sedpath = "../data/sed"
        self.sigpath = "../data/sig"

    def test_asd_reader_on_extensions(self):
        for f in os.listdir(self.asdpath):
            s = r.read_asd(os.path.join(self.asdpath, f))
            ext = os.path.splitext(f)[1]
            if ext == ".asd":
                self.assertEqual(s.name, f)
            else:
                self.assertTrue(s is None)

    def test_asd_reader_spectrum(self):
        s = r.read_asd("../data/asd/asd_00003.asd")
        self.assertEqual(s.name, "asd_00003.asd")
        self.assertFalse(s.resampled)
        self.assertFalse(s.mask)

    def test_reader(self):
        for (dirpath, dirnames, filenames) in os.walk(self.filepath):
            print(dirpath)
            for f in filenames:
                filepath = os.path.join(dirpath,f)
                print(filepath)
                spec = r.read(filepath)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
