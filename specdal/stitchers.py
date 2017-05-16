import sys
import numpy as np
import pandas as pd

debug = True

def stitch(spectrum, method="mean"):
    METHODS = ('mean')
    if method not in METHODS:
        msg = " ".join(["ERROR:", method, "not supported.\n"])
        sys.stderr.write(msg)
        return

    if method == "mean":
        spectrum.data = spectrum.data.groupby(level=0, axis=0).mean()

    return spectrum
