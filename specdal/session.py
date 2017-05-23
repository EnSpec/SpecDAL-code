import sys
from collections import OrderedDict
import numpy as np
import pandas as pd
from .readers import *
from .spectrum import Spectrum
import matplotlib.pyplot as plt

class Session(object):
    """
    Class representing a data processing session
    
    data: pd.DataFrame of multiple spectrum
    """
    def __init__(self):
        self.spectrums = OrderedDict()
        self.dirty = True # whether data needs update. 
        self.variable = "pct_reflect"
        self.selection = None
        self.groups = None
        self.history = None

    @property
    def spectrum_dict(self):
        return self._spectrums

    @property
    def spectrums(self):
        return list(self._spectrums.values())

    @spectrums.setter
    def spectrums(self, value):
        self._spectrums = OrderedDict()

    def add_spectrum(self, spectrum):
        if isinstance(spectrum, Spectrum):
            if spectrum.name in self._spectrums:
                # duplicate name
                print(spectrum.name, "already exists")
                return
            self._spectrums[spectrum.name] = spectrum
            self.dirty = True
        else: # not a Spectrum object
            pass

    def get_spectrum(self, spec_name):
        if spec_name in self.spectrum_dict:
            return self.spectrum_dict[spec_name]
        else:
            print(spec_name, "does not exist")

    @property
    def data(self):
        if self.dirty:
            colnames = [s.name for s in self.spectrums
                        if self.variable in s.data]
            data = pd.concat([s.data[self.variable] for s in
                              self.spectrums if self.variable in s.data],
                             axis=1)
            data.columns = colnames
            self._data = data
        return self._data

    @property
    def mask(self):
        return pd.DataFrame(data=[s.mask for s in self.spectrums],
                            index=[s.name for s in self.spectrums],
                            columns=['mask'])

    def group_by_separator(self, *args):
        separator = args[0]
        element_inds = list(map(int, args[1:]))
        def group_fcn(name):
            return separator.join([name.split(separator)[e] for e in element_inds])
        self.groups = self.data.groupby(by=group_fcn, axis=1)
        return self.groups

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value
    
    def __str__(self):
        return self.name

    ################################################################################
    # read/modify spectrum functions

    def read(self, filepath=None, directory=None, recursive=False,
             fmt=None):
        """ Read the raw spectrum file or directory"""
        if filepath:
            spec = read(filepath)
            if spec is not None:
                if fmt:
                    assert(spec.fmt == fmt)
                self.add_spectrum(spec)
        elif directory:
            for dirpath, dirnames, filenames in os.walk(directory):
                if not recursive:
                    if dirpath != directory:
                        continue
                for f in filenames:
                    filepath = os.path.join(dirpath, f)
                    print("Reading:", filepath, end="...")
                    spec = read(os.path.abspath(filepath))
                    if fmt:
                        assert(spec.fmt == fmt)
                    self.add_spectrum(spec)
                    print("Done")
        self.dirty = True

    def resample(self, spec_name=None, mask=True, group=None,
                 fmt=None, **kargs):
        """ Resample the spectrums in the session """
        if spec_name:
            assert(spec_name in self.spectrum_dict)
            self.spectrum_dict[spec_name].resample(**kargs)
        else:
            specs = self.spectrums
            if mask is True:
                specs = [s for s in specs if s.mask is False]
            if group:
                specs = [s for s in specs if s.group == group]
            if fmt:
                specs = [s for s in specs if s.fmt == fmt]
            for s in specs:
                print("resampling", s.name, end="...")
                s.resample(**kargs)
                print("Done")
        self.dirty=True

    def stitch(self, spec_name=None, mask=True, group=None, fmt=None,
               **kargs):
        """ Stitch the spectrums in the session """
        if spec_name:
            assert(spec_name in self.spectrum_dict)
            self.spectrum_dict[spec_name].stitch(**kargs)
        else:
            specs = self.spectrums
            if mask is True:
                specs = [s for s in specs if s.mask is False]
            if group:
                specs = [s for s in specs if s.group == group]
            if fmt:
                specs = [s for s in specs if s.fmt == fmt]
            for s in specs:
                print("stitching", s.name, end="...")
                s.stitch(**kargs)
                print("Done")
        self.dirty=True

    def jump_correct(self, spec_name=None, mask=True, group=None,
                     fmt=None, **kargs):
        """ Jump correct the spectrums in the session """
        if spec_name:
            assert(spec_name in self.spectrum_dict)
            self.spectrum_dict[spec_name].jump_correct(**kargs)
        else:
            specs = self.spectrums
            if mask is True:
                specs = [s for s in specs if s.mask is False]
            if group:
                specs = [s for s in specs if s.group == group]
            if fmt:
                specs = [s for s in specs if s.fmt == fmt]
            for s in specs:
                print("jump_correcting", s.name, end="...")
                s.jump_correct(**kargs)
                print("Done")
        self.dirty=True

    def set_mask(self, mask=False, spec_name=None, group=None, fmt=None):
        """ Set the mask """
        if spec_name:
            assert(spec_name in self.spectrum_dict)
            self.spectrum_dict[spec_name].mask = mask
        else:
            specs = self.spectrums
            if group:
                specs = [s for s in specs if s.group == group]
            if fmt:
                specs = [s for s in specs if s.fmt == fmt]
            for s in specs:
                s.mask = mask
        self.dirty=True

    ################################################################################
    # misc

    def status(self, spec_name=None):
        pass

    def save_figs(self, outdir=None, group_by=True, spec_name=None,
                  mask=None, group=None, fmt=None):
        if outdir:
            if not os.path.exists(outdir):
                os.makedirs(outdir)

        if spec_name:
            ax = self.spectrum_dict[spec_name].data[self.variable].plot()
            ax.set_ylabel('reflectance %')
            if outdir:
                plt.savefig(outdir, bbox_inches='tight')
            else:
                plt.show()
            plt.close()
        if group_by is False:
            # show all 
            pass
        else:
            for gname, gdata in self.groups:
                if group:
                    if gname not in group:
                        continue
                print("Group:", gname, end='...')
                figpath = os.path.join(outdir, gname + '.png')                
                # create figure
                ax = gdata.plot(title=gname)
                ax.set_ylabel('reflectance %')
                if outdir:
                    plt.savefig(os.path.join(figpath), bbox_inches='tight')
                else:
                    plt.show()
                plt.close()
                print("DONE")
            pass

    def save_csv(self, outdir=None, group_by=True, spec_name=None,
                 mask=None, group=None, fmt=None):
        if outdir:
            if not os.path.exists(outdir):
                os.makedirs(outdir)

        if spec_name:
            datapath = os.path.join(outdir, spec_name + '.csv')
            self.spectrum_dict[spec_name].data.transpose().to_csv(datapath)

        if group_by is False:
            # save all
            datapath = os.path.join(outdir, 'all_data' + '.csv')
            self.data.transpose().to_csv(datapath)
        else:
            for gname, gdata in self.groups:
                datapath = os.path.join(outdir, gname + '.csv')
                if group:
                    if gname not in group:
                        continue
                print("Group:", gname, end='...')
                # create figure
                gdata.transpose().to_csv(datapath)
                print("DONE")
