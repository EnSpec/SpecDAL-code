import sys
import numpy as np
import pandas as pd
import functools
from collections import OrderedDict

class Collection(object):
    """A container storing a multiple Spectrum objects.

    Parameters
    -----------

    name : string
        Name of the collection

    spectrums : OrderedDict
        key : name of Spectrum object
        value : reference to Spectrum object

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

    def __init__(self, name, spectrums=[]):
        self.name = name
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

    ##################################################
    # wrappers for Spectrum methods

    def resample(self):
        pass

    def stitch(self):
        pass

    def jump_correct(self):
        pass

    ##################################################
    # group operations
    def group_by(self, method, **kwargs):
        """
        Form groups and return a collection for each group

        Returns
        -------
        OrderedDict consisting of collection object for each group
            key: group name
            value: collection object
        """
        pass

    def aggregate(self, fcn):
        """
        Aggregate the spectrum objects by applying fcn.

        Returns
        -------
        A Spectrum object after aggregating by fcn.
        """
        pass
