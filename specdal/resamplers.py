import sys
import numpy as np
import pandas as pd

debug = False
def resample(spectrum, method="slinear"):

    METHODS = ('slinear', 'cubic')
    if method not in METHODS:
        msg = " ".join(["ERROR:", method, "not supported.\n"])
        sys.stderr.write(msg)
        return

    wavelengths = pd.Series(spectrum.data.index)
    n = len(wavelengths)

    # spectrum may have overlapping sequences
    head_positions = [0] + list(wavelengths[wavelengths.diff() < 0].index)
    tail_positions = list(wavelengths[wavelengths.diff() < 0].index) + [n]

    dataframes = []
    for sequence in zip(head_positions, tail_positions):
        # subset the dataframe corresponding to the sequence
        head_pos, tail_pos = sequence
        dataframe = spectrum.data.iloc[head_pos:tail_pos].copy()
        # expand index to all integers
        int_index = pd.Index(np.arange(np.round(wavelengths[head_pos]),
                                       np.round(wavelengths[tail_pos-1]) + 1),
                             name=spectrum.data.index.name)
        temp_index = dataframe.index.union(int_index)
        dataframe = dataframe.reindex(temp_index)
        # interpolate 
        dataframe = dataframe.interpolate(method=method)
        # select the integer indices
        dataframes.append(dataframe.loc[int_index])

        if debug:
            # plot for debugging .sig
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            dataframe.reset_index().plot.scatter(x="index", y="ref_radiances", ax=ax, c="red")
            spectrum.data.iloc[head_pos:tail_pos].reset_index().plot(x="wavelengh", y="ref_radiances", ax=ax, c="blue")
            spectrum.data.iloc[head_pos:tail_pos].reset_index().plot.scatter(x="wavelengh", y="ref_radiances", ax=ax, c="blue", s=100)
            plt.show()
            return

    spectrum.data = pd.concat(dataframes)
    spectrum.resampled = True
    return spectrum
