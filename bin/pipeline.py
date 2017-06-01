import argparse

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(".."))
from specdal.spectrum import Spectrum
from specdal.collection import Collection
from specdal import session
from specdal import readers as r

# parse command line args
parser = argparse.ArgumentParser(description="SpecDAL Pipeline")

parser.add_argument("indir", default=None, help="input directory")
parser.add_argument("outdir", default=None, help="output directory")
parser.add_argument("-res", "--resampler", choices=["slinear", "spline"],
                    default=None)
parser.add_argument("-sti", "--stitcher", choices=["mean", "blending"],
                    default=None)
parser.add_argument("-jump", "--jump_correct", nargs="*",
                    default=None,
                    help="First arg specifies the reference. "
                    "Remaining args specify the splice wavelengths. "
                    "i.e. -jump 0 1000 1800")
parser.add_argument("-gsep", "--group_by_separator", nargs="*",
                    default=None,
                    help="First arg specifies the separator. "
                    "Remaining args specify positions for forming a group",
                    metavar="separator")
parser.add_argument("-gfunc", "--group_function",
                    choices=["mean", "median", "std", "min", "max"],
                    nargs="*",
                    default=None,
                    help="Function applied to each group [average | otherstocome]",
                    metavar="gfunction")
parser.add_argument("-r", "--recursive", action="store_true",
                    default=False,
                    help="recursively walk through input directory and process files")

args = parser.parse_args()

# make output directory
outdir = os.path.abspath(args.outdir)
figdir = os.path.join(outdir, "figures")
datadir = os.path.join(outdir, "data")
for d in (outdir, figdir, datadir):
    if not os.path.exists(d):
        os.makedirs(d)
    
################################################################################
# create session

# read directory into collection
c = Collection(name="original")
c.read(path=args.indir)

# resample
c.resample()

# overlap stitch
c.stitch()

# stitch
if args.jump_correct:
    # parse command line args
    args.jump_correct = list(map(int, args.jump_correct))
    reference = args.jump_correct[0]
    splices = args.jump_correct[1:]

    # stitch
    c.jump_correct(splices, reference=reference)


# save original data and fig
c.plot()
plt.savefig(os.path.join(figdir, c.name + ".png"),  bbox_inches="tight")
plt.close()
c.to_csv(os.path.join(datadir, c.name + ".csv"))

# save mask file
maskpath = os.path.join(outdir, "mask.csv")
c.masks.to_csv(maskpath)


# group by
if args.group_by_separator:
    if args.group_function:
        if "mean" in args.group_function:
            # get a collection of grouped means
            means = c.group_by(separator=args.group_by_separator[0],
                               aggr_fcn="mean",
                               indices=args.group_by_separator[1:])
            # add averaged spectrums to original collection
            for spec in means.spectrums:
                c.add_spectrum(spec)

        if "median" in args.group_function:
            # get a collection of grouped means
            medians = c.group_by(separator=args.group_by_separator[0],
                               aggr_fcn="median",
                               indices=args.group_by_separator[1:])
            # add median spectrums to original collection
            for spec in medians.spectrums:
                c.add_spectrum(spec)

        if "std" in args.group_function:
            # get a collection of grouped std
            stds = c.group_by(separator=args.group_by_separator[0],
                               aggr_fcn="std",
                               indices=args.group_by_separator[1:])

        if "min" in args.group_function:
            # get a collection of grouped min
            mins = c.group_by(separator=args.group_by_separator[0],
                               aggr_fcn="min",
                               indices=args.group_by_separator[1:])

        if "max" in args.group_function:
            # get a collection of grouped max
            maxs = c.group_by(separator=args.group_by_separator[0],
                               aggr_fcn="max",
                               indices=args.group_by_separator[1:])

# group_by again to include averaged spectrum in each group
group_colls = c.group_by(separator=args.group_by_separator[0],
                         indices=args.group_by_separator[1:])

for group_id, group_coll in group_colls.items():
    # save group plot
    group_coll.plot()
    plt.savefig(os.path.join(figdir, group_coll.name + ".png"),  bbox_inches="tight")
    plt.close()
    # save group csv
    group_coll.to_csv(os.path.join(datadir, group_coll.name + ".csv"))

# plot of means
if means:
    means.plot()
    plt.savefig(os.path.join(figdir, means.name + ".png"),  bbox_inches="tight")
    plt.close()
    means.to_csv(os.path.join(datadir, means.name + ".csv"))

# plot of means
if medians:
    medians.plot()
    plt.savefig(os.path.join(figdir, medians.name + ".png"),  bbox_inches="tight")
    plt.close()
    medians.to_csv(os.path.join(datadir, medians.name + ".csv"))

# plot of stds
if stds:
    stds.plot()
    plt.savefig(os.path.join(figdir, stds.name + ".png"),  bbox_inches="tight")
    plt.close()
    stds.to_csv(os.path.join(datadir, stds.name + ".csv"))

# plot of mins
if mins:
    mins.plot()
    plt.savefig(os.path.join(figdir, mins.name + ".png"),  bbox_inches="tight")
    plt.close()
    mins.to_csv(os.path.join(datadir, mins.name + ".csv"))

# plot of maxs
if maxs:
    maxs.plot()
    plt.savefig(os.path.join(figdir, maxs.name + ".png"),  bbox_inches="tight")
    plt.close()
    maxs.to_csv(os.path.join(datadir, maxs.name + ".csv"))

