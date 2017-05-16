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
    
    def __init__(self, name, data=None, resampled=False, stitched=False,
                 metadata=None, mask=False):
        if data is not None:
            self.data = data
        self.name = name
        self.resampled = resampled
        self.stitched = stitched
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
    def stitched(self):
        return self._stitched

    @stitched.setter
    def stitched(self, value):
        self._stitched = value

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

    def resample(self, method="slinear"):
        METHODS = ('slinear', 'cubic')
        if method not in METHODS:
            msg = " ".join(["ERROR:", method, "not supported.\n"])
            sys.stderr.write(msg)
            return

        wavelengths = pd.Series(self.data.index)
        n = len(wavelengths)

        # spectrum may have overlapping sequences
        head_positions = [0] + list(wavelengths[wavelengths.diff() < 0].index)
        tail_positions = list(wavelengths[wavelengths.diff() < 0].index) + [n]

        dataframes = []
        for sequence in zip(head_positions, tail_positions):
            # subset the dataframe corresponding to the sequence
            head_pos, tail_pos = sequence
            dataframe = self.data.iloc[head_pos:tail_pos].copy()
            # expand index to all integers
            int_index = pd.Index(np.arange(np.round(wavelengths[head_pos]),
                                           np.round(wavelengths[tail_pos-1]) + 1),
                                 name=self.data.index.name)
            temp_index = dataframe.index.union(int_index)
            dataframe = dataframe.reindex(temp_index)
            # interpolate 
            dataframe = dataframe.interpolate(method=method)
            # select the integer indices
            dataframes.append(dataframe.loc[int_index])

        self.data = pd.concat(dataframes)
        self.resampled = True

    def stitch(self, method="mean"):
        METHODS = ('mean')
        if method not in METHODS:
            msg = " ".join(["ERROR:", method, "not supported.\n"])
            sys.stderr.write(msg)
            return

        if method == "mean":
            self.data = self.data.groupby(level=0, axis=0).mean()
        self.stitched = True
