import sys
import numpy as np
import pandas as pd
import functools
from collections import Iterable

class Spectrum(object):
    """A container storing a single spectrum measurement.

    Parameters
    -----------

    name : string
        Name of the spectrum

    reflectance : pandas Series
        Data to store measurements.

    Examples
    --------

    Raises
    ------

    Notes
    -----
    Spectrum object stores a single spectrum measurement using pandas
    Series.  By convention, the index is named as "wave" and each row
    represents specific wavelength.  There can be several columns,
    usually including "pct_reflect".

    See also
    --------

    """

    def __init__(self, name, reflectance=None):
        self.name = name
        self.reflectance = reflectance
        pass

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
    def reflectance(self):
        return self._reflectance

    @reflectance.setter
    def reflectance(self, value):
        """Setter for reflectance property.
        """
        # TODO: convert to pandas series.
        # TODO: check for valid index (index.name == "wavelength")
        self._reflectance = value

    ################################################
    # methods on reflectance
    def resample(self):
        """Interpolate to 1nm integer wavelengths"""
        pass

    def stitch(self):
        """Stitch the overlap in wavelengths"""
        pass

    def jump_correct(self):
        """Stitch jumps in reflectance for non-overlapping wavelengths"""
        pass

    ##################################################
    # operators
    def __add__(self, other):
        pass
    
    def __radd__(self):
        pass
    
    def __iadd__(self):
        pass
    
