import os
import sys
import struct
import numpy as np
import pandas as pd
from .spectrum import Spectrum

# column mapping
cols_sed = {
    'Wvl':'wavelength',
    'Rad. (Target)':'tgt_radiance',
    'Reflect. %':'pct_reflect',
    'Rad. (Ref.)':'ref_radiance',
}

def read(filepath, name=None):
    """function to call the appropriate reader for file extension
    """
    
    FORMATS = {'.asd':read_asd, '.sig':read_sig, '.sed':read_sed }
    
    if name is None:
        name = os.path.basename(filepath) + "_orig"

    ext = os.path.splitext(filepath)[1]

    if ext not in FORMATS:
        # msg = " ".join(["ERROR:", ext, "not supported.\n"])
        # sys.stderr.write(msg)
        return

    return FORMATS[ext](filepath, name)


def read_asd(filepath, name=None):
    """
    function to read .asd file

    Parameters
    ----------
    filepath: string
        Full path to .asd file.

    Returns
    -------
    Spectrum
        Spectrum object with data from file.
        None is returned if something goes wrong.
    """

    # define constants
    VERSIONS = {'ASD': None,
                'asd': None,
                'as6': None,
                'as7': None,
                'as8': None}
    SPECTRUM_TYPES = ("RAW_TYPE",
                     "REF_TYPE",
                     "RAD_TYPE",
                     "NOUNITS_TYPE",
                     "IRRAD_TYPE",
                     "QI_TYPE",
                     "TRANS_TYPE",
                     "UNKNOWN_TYPE",
                     "ABS_TYPE")
    HAS_REF = {'ASD': False,
               'asd': False,
               'as6': True,
               'as7': True,
               'as8': True}

    if name is None:
        name = os.path.basename(filepath)

    mask = False
    
    # read binary .asd file
    with open(filepath, "rb") as f:
        binconts = f.read()
        version = binconts[0:3].decode("utf-8")

        if not version in VERSIONS:
            print("ERROR:", version , "not supported.")
        else:
            # read spectrum type
            spectrum_type_index = struct.unpack("B", binconts[186:(186 + 1)])[0]
            spectrum_type = SPECTRUM_TYPES[spectrum_type_index]

            # read wavelength info
            wavestart = struct.unpack("f", binconts[191:(191 + 4)])[0]
            wavestep = struct.unpack("f", binconts[195:(195 + 4)])[0]
            num_channels = struct.unpack("h", binconts[204:(204 + 2)])[0]
            wavestop = wavestart + num_channels*wavestep - 1
            waves = np.linspace(wavestart, wavestop, num_channels)

            # read splice wavelength
            splice1 = struct.unpack("f", binconts[444:(444 + 4)])[0]
            splice2 = struct.unpack("f", binconts[448:(448 + 4)])[0]
            
            # read data
            data_format = struct.unpack("B", binconts[199:(199 + 1)])[0]
            fmt = "f"*num_channels
            if data_format == 2:
                fmt = 'd'*num_channels
            if data_format == 0:
                fmt = 'f'*num_channels
            size = num_channels*8

            # Read the spectrum block data
            spectrum = np.array(struct.unpack(fmt, binconts[484:(484 + size)]))

            # Read the join wavelengths
            join1_wave = struct.unpack("f", binconts[444:(444 + 4)])[0]
            join2_wave = struct.unpack("f", binconts[448:(448 + 4)])[0]

            reference = None
            if HAS_REF[version]:
                # read reference
                start = 484 + size
                ref_flag = struct.unpack('??', binconts[start: start + 2])[0]
                first, last = start + 18, start + 20
                ref_desc_length = struct.unpack('H', binconts[first:last])[0]
                first = start + 20 + ref_desc_length
                last = first + size
                reference = np.array(struct.unpack(fmt, binconts[first:last]))
            else:
                mask = False

            data = pd.DataFrame({"target" : spectrum,
                                 "reference": reference}, index=waves)
            data.index.name = "wavelength"

            data['pct_reflect'] = data.iloc[:, 1] / data.iloc[:, 0]

            measurement = data['pct_reflect']

            # metadata
            meta = {
                'type':spectrum_type,
                'splice':[splice1, splice2]
            }
            
            # convert data into spectrum and return
            return Spectrum(name=name, measurement=measurement)


def read_sig(filepath, name=None):
    if name is None:
        name = os.path.basename(filepath)

    with open(filepath, 'r') as f:
        meta = {}
        for i, line in enumerate(f):
            line = line.splitlines()[0].split("= ")
            if len(line) > 1:
                if line[0] == 'data':
                    if meta['units'] == "Counts, Counts":
                        colnames = ["wavelength", "ref_counts",
                                    "tgt_counts", "pct_reflect"]
                    elif meta['units'] == "Radiance, Radiance":
                        colnames = ["wavelength", "ref_radiance",
                                    "tgt_radiance", "pct_reflect"]
                    data = pd.read_table(filepath, skiprows=i+1,
                                         sep="\s+", index_col=0,
                                         header=None, names=colnames
                    )
                    measurement = data['pct_reflect']
                    return Spectrum(name=name, measurement=measurement)
                else:
                    meta[line[0]] = line[1]


def read_sed(filepath, name=None):
    """
    Note: pct_reflect sometimes doesn't match tgt/ref
    """
    mask = False
    if name is None:
        name = os.path.basename(filepath)
    with open(filepath, 'r') as f:
        meta = {}
        for i, line in enumerate(f):
            line = line.splitlines()[0].split(": ")
            if line[0] == 'Data:':
                data = pd.read_table(filepath, skiprows=i+1,
                                     sep="\t"
                )
                
                ## must have the columns: 'Wvl', 'Rad. (Target)', 'Rad. (Ref.)'
                for col in ('Wvl', 'Rad. (Target)', 'Rad. (Ref.)'):
                    if col not in data.columns:
                        mask = True

                # calculate reflectance
                if mask is not True:
                    if 'Reflect. %' not in data.columns:
                        data['Reflect. %'] = data['Rad. (Target)'] / data['Rad. (Ref.)']
                # translate column headers
                data.columns = [cols_sed[column] if column in cols_sed else column
                                for column in data.columns]
                data = data.set_index("wavelength")
                measurement = data['pct_reflect']
                return Spectrum(name=name, measurement=measurement)
                
            else:
                if len(line) > 1:
                    meta[line[0]] = line[1]
