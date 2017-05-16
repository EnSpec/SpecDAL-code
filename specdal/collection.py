import sys
from collections import OrderedDict
import numpy as np
import pandas as pd
from .spectrum import Spectrum
import matplotlib.pyplot as plt

class Collection(object):
    """
    Class representing a dataset of spectra
    
    data: pd.DataFrame of multiple spectrum
    
    """
    def __init__(self):
        self.group = None
        pass

    @property
    def spectra(self):
        if not hasattr(self, '_spectrums'):
            return
        return self._spectrums

    @property
    def data(self):
        if not hasattr(self, '_spectrums'):
            return
        return pd.concat([s.data["pct_reflect"].rename(s.name) for s in
                          self._spectrums if "pct_reflect" in s.data],
                         axis=1)

    def add_spectrum(self, spectrum):
        '''Consider OrderedDict rather than list (i.e. for setting mask)'''
        if not hasattr(self, '_spectrums'):
            self._spectrums = []
        if isinstance(spectrum, Spectrum):
            self._spectrums.append(spectrum)
        if isinstance(spectrum, list):
            [self._spectrums.append(item) for item in spectrum if
             isinstance(spectrum, Spectrum)]

    @property
    def mask(self):
        if not hasattr(self, '_spectrums'):
            return
        return pd.DataFrame(data=[s.mask for s in self._spectrums],
                            index=[s.name for s in self._spectrums],
                            columns=['mask'])

    def group_by_separator(self, *args):
        separator = args[0]
        element_inds = list(map(int, args[1:]))
        def group_fcn(name):
            return separator.join([name.split(separator)[e] for e in element_inds])
        self.group = self.data.groupby(by=group_fcn, axis=1)
        return self.group    
