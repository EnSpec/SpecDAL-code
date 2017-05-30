import sys
import numpy as np
import pandas as pd
from collections import OrderedDict
from .spectrum import Spectrum
from itertools import groupby
import copy

class Collection(object):
    """A container storing a multiple Spectrum objects.

    Parameters
    -----------

    name : string
        Name of the collection

    spectrums : list
        list of Spectrum objects

    Examples
    --------

    Raises
    ------

    Notes
    -----
    Collection object represents and operates on multiple spectrum
    measurements. specdal.Spectrum objects are stored in an OrderedDict
    which is converted to pandas.DataFrame object for operations.

    See also
    --------

    """

    def __init__(self, name, measure_type="pct_reflect", spectrums=[]):
        self.name = name
        self.measure_type = measure_type
        self.spectrums = spectrums
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """Setter for name property.
        """
        self._name = value

    @property
    def data(self):
        """return pandas dataframe of the measurement data from spectrums"""
        return pd.concat(objs=[s.measurement for s in self.spectrums],
                         axis=1,
                         keys=[s.name for s in self.spectrums])

    @property
    def spectrums_dict(self):
        """Get a dictionary of Spectrum objects"""
        return self._spectrums

    @property
    def spectrums(self):
        """Get a list of Spectrum objects"""
        return list(self._spectrums.values())

    @spectrums.setter
    def spectrums(self, value):
        """Setter for spectrums property.

        Parameters
        -----------

        value : list of spectrums
        """

        self._spectrums = OrderedDict()
        # assert value is Iterable
        for s in value:
            # assert s is Spectrum
            self._spectrums[s.name] = s

    def add_spectrum(self, spectrum):
        """add spectrum to the collection"""
        if spectrum.name in self.spectrums_dict:
            # name already exists
            return
        self._spectrums[spectrum.name] = spectrum

    def remove_spectrum(self, spectrum):
        """remove spectrum from the collection"""
        if spectrum.name in self.spectrums_dict:
            del self._spectrums[spectrum.name]


    ##################################################
    # wrappers for Spectrum methods

    def read(self):
        pass
    
    def resample(self):
        pass

    def stitch(self):
        pass

    def jump_correct(self):
        pass

    ##################################################
    # data operations
    def aggregate(self, fcn):
        """
        Aggregate the spectrum objects by applying fcn.

        Returns
        -------
        A Spectrum object after aggregating by fcn.
        """
        newname = "_".join([self.name, fcn])
        measurement = None
        if fcn == "mean":
            measurement = self.data.mean(axis=1)

        if fcn == "median":
            measurement = self.data.median(axis=1)
            
        return Spectrum(name=newname, measurement=measurement,
                        measure_type=self.measure_type)

    ##################################################
    # group operations
    def group_by(self, method="separator", **kwargs):
        """
        Form groups and return a collection for each group.

        Returns
        -------
        OrderedDict consisting of collection object for each group
            key: group name
            value: collection object

        Notes
        -----
        The result is a deepcopy of the original collection and 
        spectrums.
        """
        def group_by_separator(spectrum, fill="."):
            separator = kwargs["separator"]
            element_inds = kwargs["indices"]
            elements = spectrum.name.split(separator)
            return '_'.join([elements[i] if i in element_inds else fill
                             for i in range(len(elements))])

        KEY_FUN = {"separator": group_by_separator}
        spectrums_sorted = sorted(self.spectrums, key=lambda x: group_by_separator(x))

        result = OrderedDict()
        for g_name, g_spectrums in groupby(spectrums_sorted, KEY_FUN[method]):
            coll = Collection(name=g_name,
                              spectrums=[copy.deepcopy(s) for s in g_spectrums])
            result[coll.name] = coll
        return result
