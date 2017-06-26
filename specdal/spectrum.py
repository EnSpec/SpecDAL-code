import numpy as np
import pandas as pd
from collections import Iterable

class Spectrum(object):
    """
    A container storing a single spectrum measurement as np.array.

    Parameters
    -----------
    name : string
        Name of the spectrum.
    data : list of numpy.recarray objects
        The dataset. numpy.recarray objects
    resampled : `bool`, optional
        Indicates whether the spectrum has been resampled to integer wavelengths
    metadata : dictionary
        key:value pair for metadata

    Raises
    ------
    Notes
    -----
    See also
    --------
    """
    
    def __init__(self, name, data=None, resampled=False, metadata=None, mask=False):
        if data is not None:
            self.data = data
        self.name = name
        self.resampled = resampled
        self.mask = mask
        if metadata is not None:
            self.metadata = metadata

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, pd.DataFrame):
            self._data = value
        else:
            print("Error: data must be a pd.DataFrame object")

    @property
    def resampled(self):
        return self._resampled

    @resampled.setter
    def resampled(self, value):
        self._resampled = value

    @property
    def mask(self):
        if hasattr(self, "_mask"):        
            return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value

    @property
    def metadata(self):
        if hasattr(self, "_metadata"):
            return self._metadata

    @metadata.setter
    def metadata(self, value):
        if isinstance(value, dict):
            self._metadata = dict(value)
            return
        if not hasattr(self, "_metadata"):
            self._metadata = {}
        if isinstance(value, Iterable):
            if len(value) == 2:
                self._metadata[value[0]] = value[1]
