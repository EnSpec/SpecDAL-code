import sys
import numpy as np
import pandas as pd
import functools
from collections import Iterable

class Spectrum(object):
    """
    A container storing a single spectrum measurement.

    Parameters
    -----------

    name : string
        Name of the spectrum
    data : pandas DataFrame
        Data to store measurements.
    group : string
        indicates group. Can be dynamically modified.
    fmt : string
        original file format 
    mask : bool
        boolean indicating whether spectrum is masked
    resampled : bool
        boolean indicating whether spectrum is resampled
    stitched : bool
        boolean indicating whether spectrum is stitched
    metadata : dict
        dict containing metadata        
    history : dict
        dict containing methods called on this object

    Examples
    --------
    Raises
    ------
    Notes
    -----
    Spectrum object stores a single spectrum measurement using pandas DataFrame.
    By convention, the index is named as "wave" and each row represents specific 
    wavelength. 
    There can be several columns, usually including "pct_reflect".

    See also
    --------
    """
    
    def __init__(self, name, fmt=None, mask=False, resampled=False, stitched=False,
                 group=None, data=None, metadata=None):
        self.name = name
        self.fmt = fmt
        self.mask = mask
        self.resampled = resampled
        self.stitched = stitched
        if group is None:
            self.group = name
        else:
            self.group = group
        if data is not None:
            self.data = data
        if metadata is not None:
            self.metadata = metadata
        self.history = []

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
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value
        
    @property
    def fmt(self):
        return self._fmt

    @fmt.setter
    def fmt(self, value):
        if value not in ("asd", "sed", "sig"):
            self.mask = True
        self._fmt = value
        
    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value

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
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if isinstance(value, dict):
            self._metadata = dict(value)
            return
        if isinstance(value, Iterable):
            if len(value) == 2:
                self._metadata[value[0]] = value[1]

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value
    
    def __str__(self):
        return self.name

    ################################################################################
    # methods on spectral data
    
    def resample(self, method="slinear"):
        """ interpolate the data into integer (1nm) wavelengths """
        self.history.append(functools.partial(self.resample, method))
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

    def stitch(self, method="mean", waves=None, reference=None):
        """ Stitch the overlapping regions """
        self.history.append(functools.partial(self.stitch, method, waves, reference))
        METHODS = ('mean')
        if method not in METHODS:
            msg = " ".join(["ERROR:", method, "not supported.\n"])
            sys.stderr.write(msg)
            return
        
        if method == "mean":
            self.data = self.data.groupby(level=0, axis=0).mean()

    def jump_correct(self, waves, reference, method="additive"):
        """ Perform jump correction (no overlap) """
        if method == "additive":
            self._jump_correct_additive(waves, reference)
        else:
            print(method, "method is not supported")
            return

    def _jump_correct_additive(self, waves, reference):
        """ Perform additive jump correction (ASD) """
        # if asd, get the locations from the metadata
        # stop if overlap exists
        def get_sequence(wave):
            # this function might need to be more generic: utils.py?
            for i, w in enumerate(waves):
                if wave <= w:
                    return i
            return i+1
        def translate_y(ref, mov, right=True):
            # translates the mov dataframe to stitch with ref
            # what happens if multiple columns?
            if right:
                diff = ref.iloc[-1] - mov.iloc[0]
            else:
                diff = ref.iloc[0] - mov.iloc[-1]
            mov = mov + diff
            self.data.update(mov)
            
        groups = self.data.groupby(get_sequence)
        
        for i in range(reference, groups.ngroups-1, 1):
            translate_y(groups.get_group(i),
                        groups.get_group(i+1),
                        right=True)

        for i in range(reference, 0, -1):
            translate_y(groups.get_group(i),
                        groups.get_group(i-1),
                        right=False)
            
        self.stitched = True
