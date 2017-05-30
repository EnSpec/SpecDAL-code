import sys
from collections import OrderedDict
import numpy as np
import pandas as pd
from .readers import *
from .spectrum import Spectrum
from .collection import Collection
import matplotlib.pyplot as plt

class Session(object):
    """A class representing a data processing session.

    Parameters
    -----------

    name : string
        Name of the spectrum

    Examples
    --------

    Raises
    ------

    Notes
    -----

    See also
    --------

    """
    def __init__(self):
        self.collections = OrderedDict()

    @property
    def collections(self):
        return list(self._collections.values())

    @property
    def collections_dict(self):
        return self._collections

    @collections.setter
    def collections(self, value):
        self._collections = OrderedDict()
        # assert value is iterable
        for c in value:
            # assert c is a collection
            self._collections[c.name] = c
