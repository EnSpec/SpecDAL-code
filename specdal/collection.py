import sys
import os
import numpy as np
import pandas as pd
from collections import OrderedDict
from .spectrum import Spectrum
from .readers import *
from itertools import groupby
from matplotlib import pyplot as plt
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

    def __init__(self, name, measure_type="pct_reflect", spectrums=[], masks={}):
        self.name = name
        self.measure_type = measure_type
        self.spectrums = spectrums
        self.masks = masks

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

    def add_spectrum(self, spectrum, mask=False):
        """add spectrum to the collection"""
        if spectrum.name in self.spectrums_dict:
            # name already exists
            return
        self._spectrums[spectrum.name] = spectrum
        self.masks_dict[spectrum.name] = False

    def remove_spectrum(self, spectrum):
        """remove spectrum from the collection"""
        if spectrum.name in self.spectrums_dict:
            del self._spectrums[spectrum.name]

    def get_spectrum(self, spec_name):
        """ get spectrum by name """
        if spec_name in self.spectrums_dict:
            return self.spectrums_dict[spec_name]

    @property
    def masks(self):
        """Get a dataframe of masks"""
        # return self._masks
        return pd.Series(self._masks)

    @property
    def masks_dict(self):
        """Get a dictionary of masks"""
        return self._masks

    @masks.setter
    def masks(self, value):
        self._masks = OrderedDict()
        for name in self.spectrums_dict:
            # set to false by default
            self._masks[name] = False

    def set_mask(self, name, value):
        if name not in self.spectrums_dict:
            return
        if value in [True, False]:
            self._masks[name] = value

    ##################################################
    # wrappers for Spectrum methods

    def read(self, path, ext=[".asd", ".sed", ".sig"],
             recursive=False):
        """ read all files in path that matches ext
        """
        for dirpath, dirnames, filenames in os.walk(path):
            if not recursive:
                # only read given path
                if dirpath != path:
                    continue
            for f in filenames:
                _, f_ext = os.path.splitext(f)
                if f_ext not in list(ext):
                    # skip to next file
                    continue
                filepath = os.path.join(path, f)
                spectrum = read(os.path.abspath(filepath))
                if spectrum is None:
                    pass
                else:
                    self.add_spectrum(spectrum)

    def resample(self, method="slinear"):
        for spectrum in self.spectrums:
            spectrum.resample(method=method)

    def stitch(self, method="mean"):
        for spectrum in self.spectrums:
            spectrum.stitch(method=method)
        pass

    def jump_correct(self, splices, reference, method="additive"):
        for spectrum in self.spectrums:
            spectrum.jump_correct(splices=splices,
                                  reference=reference,
                                  method=method)

    ##################################################
    # data operations

    # aggregate functions
    @property
    def mean(self):
        return Spectrum(name=self.name + "_mean", measurement=self.data.mean(axis=1))

    @property
    def median(self):
        return Spectrum(name=self.name + "_median", measurement=self.data.median(axis=1))

    @property
    def min(self):
        return Spectrum(name=self.name + "_min", measurement=self.data.min(axis=1))

    @property
    def max(self):
        return Spectrum(name=self.name + "_max", measurement=self.data.max(axis=1))

    @property
    def std(self):
        return Spectrum(name=self.name + "_std", measurement=self.data.std(axis=1))

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
        or
        Collection of aggregate if aggr_fcn is supplied

        Notes
        -----
        The result is a deepcopy of the original collection and 
        spectrums.
        """
        def group_by_separator(spectrum, fill=".", **kwargs):
            separator = kwargs["separator"]
            element_inds = kwargs["indices"]
            elements = spectrum.name.split(separator)
            result = '_'.join([elements[i] if i in element_inds else
                          fill for i in range(len(elements))])
            return result

        KEY_FUN = {"separator" : group_by_separator}
        spectrums_sorted = sorted(self.spectrums, key=lambda x: group_by_separator(x, **kwargs))
        groups = groupby(spectrums_sorted, lambda x : KEY_FUN[method](x, **kwargs))

        # default result
        result = OrderedDict()
        for g_name, g_spectrums in groups:
            coll = Collection(name=g_name,
                              spectrums=[copy.deepcopy(s) for s in g_spectrums])
            result[coll.name] = coll

        return result  # OrderedDict of group collections


    ##################################################
    # wrappers for dataframe functions
    def plot(self, stats=[], **kwargs):
        title = self.name
        if "title" in kwargs:
            title = kwargs["title"]
            del kwargs["title"]
        fig, ax = plt.subplots(1, 1)
        self.data.plot(title=title, ax=ax, **kwargs)
        for stat in stats:
            if stat == "mean":
                self.mean.plot(ax=ax)
            if stat == "median":
                self.median.plot(ax=ax)
            if stat == "min":
                self.min.plot(ax=ax)
            if stat == "max":
                self.max.plot(ax=ax)
            if stat == "std":
                self.std.plot(ax=ax)

    def to_csv(self, path=None, **kwargs):
        self.data.transpose().to_csv(path_or_buf=path, **kwargs)
