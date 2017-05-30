import sys
import numpy as np
import pandas as pd
import functools
from collections import Iterable
from .utils import get_monotonic_series

class Spectrum(object):
    """A container storing a single spectrum measurement.

    Parameters
    -----------

    name : string
        Name of the spectrum

    measure_type : string
        Type of measurement. Defaults to "pct_reflect"

    measurement : pandas Series
        Data to store measurements.

    Examples
    --------

    Raises
    ------

    Notes
    -----
    Spectrum object stores a single spectrum measurement using pandas
    Series.  By convention, the index is named as "wavelength" and each row
    represents specific wavelength.  There can be several columns,
    usually including "pct_reflect".

    See also
    --------

    """
    
    def __init__(self, name="", measurement=None, measure_type="pct_reflect"):
        self.name = name
        self.measure_type = measure_type
        self.measurement = measurement

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """Setter for name property.
        """
        # TODO: assert valid separator: "_"
        self._name = value

    @property
    def measurement(self):
        # check Series
        if isinstance(self._measurement, pd.Series):
            # check index
            if self._measurement.index.name != "wavelength":
                return None
            # check variable
            if self._measurement.name != self.measure_type:
                return None
            return self._measurement

    @measurement.setter
    def measurement(self, value):
        """Setter for measurement property.
        """
        # convert to pandas series.
        if not isinstance(value, pd.Series):
            value = pd.Series(value)
            # TODO: catch exception if failed
        value.index.name = "wavelength"
        value.name = self.measure_type
        self._measurement = value

    ################################################
    # methods on measurement
    
    def resample(self, method="slinear"):
        """ Resample the measurement to 1 nm integer wavelengths
        
        notes
        -----
        The resulting measurement may be slightly smaller as it is 
        unclear how to interpolate the end points. This depends on 
        which way the endpoint rounds.
            i.e. The first measurement is on wavelength=5.1
                 Estimate for 5.0 is an EXtrapolation. How to?
        """
        seqs = []
        # account for jumps and overlaps
        for seq in get_monotonic_series(self.measurement):
            int_index = np.round(seq.index)
            tmp_index = seq.index.union(int_index)
            seq = seq.reindex(tmp_index)
            # interpolate
            seq = seq.interpolate(method=method)
            # select the integer indices
            seqs.append(seq.loc[int_index])

        self.measurement = pd.concat(seqs).dropna()

    def stitch(self, method="mean"):
        """Stitch the overlap in wavelengths"""
        if method == "mean":
            self.measurement = self.measurement.groupby(level=0, axis=0).mean()
        pass

    def jump_correct(self, splices, reference, method="additive"):
        """Stitch jumps in measurement for non-overlapping wavelengths"""
        
        if method == "additive":
            self._jump_correct_additive(splices, reference)
        else:
            print(method, "method is not supported")
            return

    def _jump_correct_additive(self, splices, reference):
        """ Perform additive jump correction (ASD) """
        # if asd, get the locations from the metadata
        # stop if overlap exists
        def get_sequence_num(wavelength):
            """ return the sequence id after cutting at splices """
            for i, splice in enumerate(splices):
                if wavelength <= splice:
                    return i
            return i+1

        def translate_y(ref, mov, right=True):
            # translates the mov sequence to stitch with ref sequence
            if right:
                diff = ref.iloc[-1] - mov.iloc[0]
            else:
                diff = ref.iloc[0] - mov.iloc[-1]
            mov = mov + diff
            self.measurement.update(mov)
            
        groups = self.measurement.groupby(get_sequence_num)

        for i in range(reference, groups.ngroups-1, 1):
            # move sequences on the right of reference
            translate_y(groups.get_group(i),
                        groups.get_group(i+1),
                        right=True)

        for i in range(reference, 0, -1):
            # move sequences on the left of reference
            translate_y(groups.get_group(i),
                        groups.get_group(i-1),
                        right=False)

    ##################################################
    # operators
    def __add__(self, other):
        pass
    
    def __radd__(self):
        pass
    
    def __iadd__(self):
        pass
