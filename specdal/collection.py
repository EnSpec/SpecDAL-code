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
        return list(self._spectrums.values())

    @property
    def data(self):
        if not hasattr(self, '_spectrums'):
            return
        
        colnames = [name for name, spec in self._spectrums.items()
                    if "pct_reflect" in spec.data]
        data = pd.concat([spec.data["pct_reflect"] for name, spec in
                          self._spectrums.items() if "pct_reflect" in spec.data],
                         axis=1)
        data.columns = colnames
        return data

    def add_spectrum(self, spectrum):
        '''Consider OrderedDict rather than list (i.e. for setting mask)'''
        if not hasattr(self, '_spectrums'):
            self._spectrums = OrderedDict()
        if isinstance(spectrum, Spectrum):
            if spectrum.name in self._spectrums:
                # duplicate name
                print(spectrum.name, "is already in collection")
                return
            self._spectrums[spectrum.name] = spectrum
        # if isinstance(spectrum, list):
        #     [self._spectrums.append(item) for item in spectrum if
        #      isinstance(spectrum, Spectrum)]

    @property
    def mask(self):
        if not hasattr(self, '_spectrums'):
            return
        return pd.DataFrame(data=[s.mask for _, s in self._spectrums.items()],
                            index=[s.name for _, s in self._spectrums.items()],
                            columns=['mask'])

    def group_by_separator(self, *args):
        separator = args[0]
        element_inds = list(map(int, args[1:]))
        def group_fcn(name):
            return separator.join([name.split(separator)[e] for e in element_inds])
        self.group = self.data.groupby(by=group_fcn, axis=1)
        return self.group    
